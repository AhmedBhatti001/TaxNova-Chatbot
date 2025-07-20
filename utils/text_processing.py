"""
Text processing utilities for TaxNova Chatbot
Handles text cleaning, formatting, and tax-specific processing
"""

import re
from typing import List, Dict, Any
from datetime import datetime

class TextProcessor:
    """Text processing utilities for tax queries"""
    
    def __init__(self):
        self.tax_keywords = {
            'rates': ['rate', 'slab', 'percentage', 'percent', '%'],
            'deductions': ['deduction', 'exemption', 'allowance', 'rebate'],
            'filing': ['file', 'return', 'deadline', 'submit', 'iris'],
            'calculation': ['calculate', 'compute', 'amount', 'how much'],
            'withholding': ['withholding', 'advance tax', 'deduct at source'],
            'salary': ['salary', 'wage', 'employment', 'employee'],
            'business': ['business', 'profit', 'commercial', 'trade'],
            'capital_gains': ['capital gain', 'property', 'investment']
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for processing
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\?\!,]', '', text)
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract tax-related keywords from text"""
        cleaned_text = self.clean_text(text)
        found_keywords = []
        
        for category, keywords in self.tax_keywords.items():
            for keyword in keywords:
                if keyword in cleaned_text:
                    found_keywords.append(category)
                    break
        
        return found_keywords
    
    def categorize_query(self, text: str) -> str:
        """Categorize the tax query based on content"""
        keywords = self.extract_keywords(text)
        
        if not keywords:
            return "general"
        
        # Priority-based categorization
        if "calculation" in keywords:
            return "calculation"
        elif "rates" in keywords:
            return "rates"
        elif "filing" in keywords:
            return "filing"
        elif "deductions" in keywords:
            return "deductions"
        elif "withholding" in keywords:
            return "withholding"
        else:
            return keywords[0]
    
    def extract_numbers(self, text: str) -> List[float]:
        """Extract numerical values from text"""
        # Pattern to match numbers (including decimals and commas)
        pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b'
        matches = re.findall(pattern, text)
        
        numbers = []
        for match in matches:
            try:
                # Remove commas and convert to float
                number = float(match.replace(',', ''))
                numbers.append(number)
            except ValueError:
                continue
        
        return numbers
    
    def format_currency(self, amount: float) -> str:
        """Format amount as Pakistani Rupees"""
        if amount >= 10000000:  # 1 crore
            crores = amount / 10000000
            return f"Rs. {crores:.2f} crore"
        elif amount >= 100000:  # 1 lakh
            lakhs = amount / 100000
            return f"Rs. {lakhs:.2f} lakh"
        else:
            return f"Rs. {amount:,.0f}"
    
    def format_response(self, response: str, query_category: str) -> str:
        """Format the response based on query category"""
        if not response:
            return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
        
        # Add category-specific formatting
        if query_category == "rates":
            response = self._format_rates_response(response)
        elif query_category == "calculation":
            response = self._format_calculation_response(response)
        elif query_category == "filing":
            response = self._format_filing_response(response)
        
        return response
    
    def _format_rates_response(self, response: str) -> str:
        """Format tax rates response"""
        # Add emoji and structure for rates
        if "slab" in response.lower() or "rate" in response.lower():
            response = f"📊 **Tax Rates Information**\n\n{response}"
        return response
    
    def _format_calculation_response(self, response: str) -> str:
        """Format calculation response"""
        response = f"🧮 **Tax Calculation**\n\n{response}"
        return response
    
    def _format_filing_response(self, response: str) -> str:
        """Format filing response"""
        response = f"📋 **Filing Information**\n\n{response}"
        return response
    
    def validate_query(self, text: str) -> Dict[str, Any]:
        """Validate and analyze the input query"""
        if not text or len(text.strip()) < 3:
            return {
                "valid": False,
                "reason": "Query too short",
                "suggestion": "Please provide a more detailed question about Pakistan's tax system."
            }
        
        if len(text) > 500:
            return {
                "valid": False,
                "reason": "Query too long",
                "suggestion": "Please keep your question under 500 characters for better processing."
            }
        
        # Check for tax-related content
        keywords = self.extract_keywords(text)
        if not keywords and not any(word in text.lower() for word in ['tax', 'pakistan', 'fbr', 'income']):
            return {
                "valid": True,
                "warning": "Your query doesn't seem to be tax-related. I specialize in Pakistan's tax system.",
                "category": "general"
            }
        
        return {
            "valid": True,
            "category": self.categorize_query(text),
            "keywords": keywords
        }

# Global instance
text_processor = TextProcessor()

def process_query(text: str) -> Dict[str, Any]:
    """Main function to process user query"""
    return text_processor.validate_query(text)

def format_response(response: str, category: str = "general") -> str:
    """Main function to format response"""
    return text_processor.format_response(response, category)

