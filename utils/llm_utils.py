"""
LLM utilities for TaxNova Chatbot
Handles communication with various LLM providers
"""

import os
import requests
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from .text_processing import text_processor
from tax_data.pakistan_tax_data import pakistan_tax_data

# Load environment variables
load_dotenv()

class LLMProvider:
    """Enhanced LLM provider with Pakistan tax integration"""
    
    def __init__(self):
        self.provider = os.getenv('LLM_PROVIDER', 'huggingface')
        self.max_tokens = int(os.getenv('MAX_TOKENS', 500))
        self.temperature = float(os.getenv('TEMPERATURE', 0.7))
    
    def get_response(self, prompt: str, context: str = "") -> str:
        """Get enhanced response from LLM provider with tax data integration"""
        # Validate and process the query
        query_analysis = text_processor.validate_query(prompt)
        
        if not query_analysis["valid"]:
            return f"⚠️ {query_analysis['reason']}: {query_analysis['suggestion']}"
        
        # Check if we can answer with structured data first
        structured_response = self._get_structured_response(prompt, query_analysis)
        if structured_response:
            return structured_response
        
        # Otherwise, use LLM
        if self.provider == 'huggingface':
            response = self._huggingface_response(prompt, context, query_analysis)
        elif self.provider == 'openrouter':
            response = self._openrouter_response(prompt, context, query_analysis)
        elif self.provider == 'openai':
            response = self._openai_response(prompt, context, query_analysis)
        else:
            response = self._fallback_response(prompt, query_analysis)
        
        # Format the response based on query category
        category = query_analysis.get("category", "general")
        return text_processor.format_response(response, category)
    
    def _get_structured_response(self, prompt: str, analysis: Dict[str, Any]) -> Optional[str]:
        """Get structured response for common queries without LLM"""
        prompt_lower = prompt.lower()
        category = analysis.get("category", "general")
        
        # Tax calculation requests
        if category == "calculation":
            numbers = text_processor.extract_numbers(prompt)
            if numbers and len(numbers) >= 1:
                income = numbers[0]
                if income > 0:
                    calc_result = pakistan_tax_data.calculate_income_tax(income)
                    return self._format_tax_calculation(calc_result)
        
        # Tax slabs/rates requests
        if category == "rates" or any(word in prompt_lower for word in ['slab', 'rate', 'bracket']):
            return pakistan_tax_data.get_tax_slab_info()
        
        # Filing deadline requests
        if category == "filing" or any(word in prompt_lower for word in ['deadline', 'due date', 'when to file']):
            return pakistan_tax_data.get_filing_deadlines()
        
        # Deductions requests
        if category == "deductions" or any(word in prompt_lower for word in ['deduction', 'exemption', 'allowance']):
            return pakistan_tax_data.get_deductions_info()
        
        return None
    
    def _format_tax_calculation(self, calc_result: Dict[str, Any]) -> str:
        """Format tax calculation results"""
        response = f"🧮 **Tax Calculation Results**\n\n"
        response += f"**Gross Income:** Rs. {calc_result['gross_income']:,.0f}\n"
        response += f"**Total Tax:** Rs. {calc_result['total_tax']:,.0f}\n"
        response += f"**Net Income:** Rs. {calc_result['net_income']:,.0f}\n"
        response += f"**Effective Tax Rate:** {calc_result['effective_rate']:.2f}%\n\n"
        
        if calc_result['breakdown']:
            response += "**Tax Breakdown by Slab:**\n"
            for item in calc_result['breakdown']:
                response += f"• {item['slab']}: {item['rate']}% on Rs. {item['taxable_amount']:,.0f} = Rs. {item['tax']:,.0f}\n"
        
        response += "\n*Note: This is a basic calculation. Actual tax may vary based on deductions, exemptions, and other factors.*"
        return response
    
    def _huggingface_response(self, prompt: str, context: str, analysis: Dict[str, Any]) -> str:
        """Get response from HuggingFace Inference API"""
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            return self._fallback_response(prompt, analysis)
        
        model = os.getenv('DEFAULT_MODEL', 'microsoft/DialoGPT-medium')
        url = f"https://api-inference.huggingface.co/models/{model}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Enhanced context with category-specific information
        tax_context = self._get_enhanced_tax_context(analysis.get("category", "general"))
        full_prompt = f"{tax_context}\n\nUser Question: {prompt}\n\nAnswer:"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature,
                "return_full_text": False,
                "do_sample": True
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '').strip()
                    if generated_text:
                        return generated_text
                return "I'm sorry, I couldn't generate a proper response. Please try again."
            elif response.status_code == 503:
                return "The AI model is currently loading. Please try again in a moment."
            else:
                return self._fallback_response(prompt, analysis)
        except Exception as e:
            print(f"HuggingFace API Error: {e}")
            return self._fallback_response(prompt, analysis)
    
    def _openrouter_response(self, prompt: str, context: str, analysis: Dict[str, Any]) -> str:
        """Get response from OpenRouter API"""
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return self._fallback_response(prompt, analysis)
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://taxnova-chatbot.streamlit.app",
            "X-Title": "TaxNova Chatbot"
        }
        
        tax_context = self._get_enhanced_tax_context(analysis.get("category", "general"))
        
        payload = {
            "model": "microsoft/DialoGPT-medium",
            "messages": [
                {"role": "system", "content": tax_context},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return self._fallback_response(prompt, analysis)
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return self._fallback_response(prompt, analysis)
    
    def _openai_response(self, prompt: str, context: str, analysis: Dict[str, Any]) -> str:
        """Get response from OpenAI API"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return self._fallback_response(prompt, analysis)
            
            client = openai.OpenAI(api_key=api_key)
            tax_context = self._get_enhanced_tax_context(analysis.get("category", "general"))
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": tax_context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return self._fallback_response(prompt, analysis)
    
    def _get_enhanced_tax_context(self, category: str) -> str:
        """Get enhanced Pakistan tax context based on query category"""
        base_context = """You are TaxNova, an AI assistant specialized in Pakistan's Income Tax system. 
        You help users understand Pakistan's tax laws, regulations, and procedures based on the Income Tax Ordinance 2001 and recent amendments.
        
        Always provide accurate, helpful information specific to Pakistan's tax system. If unsure about specific details, 
        recommend consulting with a tax professional or the FBR website."""
        
        if category == "rates":
            base_context += f"\n\nCurrent tax slabs for individuals:\n{pakistan_tax_data.get_tax_slab_info()}"
        elif category == "filing":
            base_context += f"\n\nFiling deadlines:\n{pakistan_tax_data.get_filing_deadlines()}"
        elif category == "deductions":
            base_context += f"\n\nCommon deductions:\n{pakistan_tax_data.get_deductions_info()}"
        
        return base_context
    
    def _fallback_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Enhanced fallback response with category-specific information"""
        category = analysis.get("category", "general")
        prompt_lower = prompt.lower()
        
        # Category-specific responses
        if category == "rates" or any(word in prompt_lower for word in ['tax rate', 'tax slab', 'income tax rate']):
            return pakistan_tax_data.get_tax_slab_info()
        
        elif category == "filing" or any(word in prompt_lower for word in ['filing', 'return', 'deadline']):
            return pakistan_tax_data.get_filing_deadlines()
        
        elif category == "deductions" or any(word in prompt_lower for word in ['deduction', 'exemption']):
            return pakistan_tax_data.get_deductions_info()
        
        elif category == "calculation":
            numbers = text_processor.extract_numbers(prompt)
            if numbers and len(numbers) >= 1:
                income = numbers[0]
                if income > 0:
                    calc_result = pakistan_tax_data.calculate_income_tax(income)
                    return self._format_tax_calculation(calc_result)
        
        # General fallback
        return """I'm currently running in offline mode, but I can still help with basic Pakistan tax information:

📊 **Ask me about:**
• Current income tax rates and slabs
• Tax filing deadlines and procedures  
• Common deductions and exemptions
• Basic tax calculations
• Withholding tax information

🔧 **For AI-powered responses:**
• Configure your API keys in the .env file
• Supported providers: HuggingFace, OpenRouter, OpenAI

🏛️ **For detailed tax advice:**
• Visit the FBR website (fbr.gov.pk)
• Consult with a qualified tax advisor
• Check the Income Tax Ordinance 2001

Try asking specific questions like "What are the current tax slabs?" or "When is the filing deadline?"
"""

# Global instance
llm_provider = LLMProvider()

def get_llm_response(prompt: str, context: str = "") -> str:
    """Main function to get enhanced LLM response"""
    return llm_provider.get_response(prompt, context)

