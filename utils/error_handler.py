"""
Error handling utilities for TaxNova Chatbot
Provides robust error handling and logging
"""

import logging
import traceback
from typing import Dict, Any, Optional
from datetime import datetime
import os

class ErrorHandler:
    """Centralized error handling for the chatbot"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/taxnova.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TaxNova')
    
    def handle_api_error(self, error: Exception, provider: str) -> str:
        """Handle API-related errors"""
        error_msg = str(error)
        self.logger.error(f"API Error ({provider}): {error_msg}")
        
        if "timeout" in error_msg.lower():
            return "⏱️ The request timed out. Please try again in a moment."
        elif "rate limit" in error_msg.lower():
            return "🚫 API rate limit exceeded. Please wait a moment before trying again."
        elif "unauthorized" in error_msg.lower() or "401" in error_msg:
            return "🔑 API authentication failed. Please check your API key configuration."
        elif "503" in error_msg or "service unavailable" in error_msg.lower():
            return "🔧 The AI service is temporarily unavailable. Please try again later."
        else:
            return "❌ An error occurred while processing your request. Please try again."
    
    def handle_validation_error(self, error: Exception, user_input: str) -> str:
        """Handle input validation errors"""
        self.logger.warning(f"Validation Error: {error} for input: {user_input[:100]}...")
        return "⚠️ Please check your input and try again. Make sure your question is clear and specific."
    
    def handle_calculation_error(self, error: Exception, income: float) -> str:
        """Handle tax calculation errors"""
        self.logger.error(f"Calculation Error: {error} for income: {income}")
        return "🧮 There was an error calculating the tax. Please verify the income amount and try again."
    
    def handle_general_error(self, error: Exception, context: str = "") -> str:
        """Handle general application errors"""
        error_trace = traceback.format_exc()
        self.logger.error(f"General Error in {context}: {error}\n{error_trace}")
        
        return """🔧 I encountered an unexpected error. Here are some things you can try:

• Refresh the page and try again
• Check your internet connection
• Verify your API configuration
• Try a simpler question

If the problem persists, please contact support."""
    
    def log_user_interaction(self, user_input: str, response: str, response_time: float):
        """Log user interactions for analytics"""
        self.logger.info(f"User Query: {user_input[:100]}... | Response Time: {response_time:.2f}s")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        # This would typically read from log files or a database
        return {
            "total_errors": 0,
            "api_errors": 0,
            "validation_errors": 0,
            "calculation_errors": 0,
            "last_error": None
        }

class SafeExecutor:
    """Safe execution wrapper for critical operations"""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
    
    def safe_api_call(self, func, *args, **kwargs) -> tuple[bool, Any]:
        """Safely execute API calls with error handling"""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            error_msg = self.error_handler.handle_api_error(e, kwargs.get('provider', 'unknown'))
            return False, error_msg
    
    def safe_calculation(self, func, *args, **kwargs) -> tuple[bool, Any]:
        """Safely execute tax calculations"""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            error_msg = self.error_handler.handle_calculation_error(e, kwargs.get('income', 0))
            return False, error_msg
    
    def safe_validation(self, func, *args, **kwargs) -> tuple[bool, Any]:
        """Safely execute input validation"""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            error_msg = self.error_handler.handle_validation_error(e, kwargs.get('user_input', ''))
            return False, error_msg

# Global instances
error_handler = ErrorHandler()
safe_executor = SafeExecutor(error_handler)

def handle_error(error: Exception, error_type: str = "general", **kwargs) -> str:
    """Main error handling function"""
    if error_type == "api":
        return error_handler.handle_api_error(error, kwargs.get('provider', 'unknown'))
    elif error_type == "validation":
        return error_handler.handle_validation_error(error, kwargs.get('user_input', ''))
    elif error_type == "calculation":
        return error_handler.handle_calculation_error(error, kwargs.get('income', 0))
    else:
        return error_handler.handle_general_error(error, kwargs.get('context', ''))

def log_interaction(user_input: str, response: str, response_time: float):
    """Log user interaction"""
    error_handler.log_user_interaction(user_input, response, response_time)

