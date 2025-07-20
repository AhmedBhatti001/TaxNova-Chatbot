# TaxNova API Documentation

## Overview

TaxNova provides a modular API structure for tax-related queries and calculations. This documentation covers the internal API structure and functions available for developers who want to extend or integrate with TaxNova.

## Core Modules

### 1. LLM Utils (`utils/llm_utils.py`)

#### `get_llm_response(prompt: str, context: str = "") -> str`

Main function to get AI-powered responses for tax queries.

**Parameters:**
- `prompt` (str): User's tax-related question
- `context` (str, optional): Additional context for the query

**Returns:**
- `str`: Formatted response from the AI system

**Example:**
```python
from utils.llm_utils import get_llm_response

response = get_llm_response("What are the current tax rates?")
print(response)
```

#### `LLMProvider` Class

Core class handling multiple LLM provider integrations.

**Methods:**

##### `get_response(prompt: str, context: str = "") -> str`
Get enhanced response with tax data integration.

##### `_get_structured_response(prompt: str, analysis: Dict[str, Any]) -> Optional[str]`
Get structured response for common queries without LLM.

##### `_format_tax_calculation(calc_result: Dict[str, Any]) -> str`
Format tax calculation results for display.

### 2. Pakistan Tax Data (`tax_data/pakistan_tax_data.py`)

#### `get_tax_calculation(income: float) -> Dict[str, Any]`

Calculate income tax based on Pakistan's current tax slabs.

**Parameters:**
- `income` (float): Annual income in PKR

**Returns:**
- `Dict[str, Any]`: Tax calculation breakdown

**Example:**
```python
from tax_data.pakistan_tax_data import get_tax_calculation

result = get_tax_calculation(2000000)
print(f"Total Tax: Rs. {result['total_tax']:,.0f}")
print(f"Effective Rate: {result['effective_rate']:.2f}%")
```

**Response Structure:**
```json
{
    "total_tax": 125000.0,
    "effective_rate": 6.25,
    "breakdown": [
        {
            "slab": "Rs. 600,001 - Rs. 1,200,000",
            "rate": 2.5,
            "taxable_amount": 600000,
            "tax": 15000
        }
    ],
    "net_income": 1875000.0,
    "gross_income": 2000000.0
}
```

#### `get_tax_slabs() -> str`

Get formatted current tax slabs information.

**Returns:**
- `str`: Formatted tax slabs for display

#### `get_filing_info() -> str`

Get filing deadlines information.

**Returns:**
- `str`: Formatted filing information

#### `get_deductions() -> str`

Get deductions and exemptions information.

**Returns:**
- `str`: Formatted deductions information

#### `PakistanTaxData` Class

Core class containing Pakistan tax system data and calculations.

**Properties:**
- `current_tax_year`: Current tax year (e.g., "2024-25")
- `tax_slabs`: List of tax slab dictionaries
- `important_dates`: Dictionary of filing deadlines
- `deductions`: Dictionary of available deductions
- `withholding_rates`: Dictionary of withholding tax rates

**Methods:**

##### `calculate_income_tax(annual_income: float) -> Dict[str, Any]`
Calculate comprehensive income tax breakdown.

##### `get_tax_slab_info() -> str`
Get formatted tax slab information.

##### `get_filing_deadlines() -> str`
Get formatted filing deadlines.

##### `get_deductions_info() -> str`
Get formatted deductions information.

### 3. Text Processing (`utils/text_processing.py`)

#### `process_query(text: str) -> Dict[str, Any]`

Process and validate user query.

**Parameters:**
- `text` (str): User input text

**Returns:**
- `Dict[str, Any]`: Query analysis results

**Example:**
```python
from utils.text_processing import process_query

analysis = process_query("What are the tax rates?")
print(f"Category: {analysis['category']}")
print(f"Valid: {analysis['valid']}")
```

**Response Structure:**
```json
{
    "valid": true,
    "category": "rates",
    "keywords": ["rates"],
    "warning": null
}
```

#### `format_response(response: str, category: str = "general") -> str`

Format response based on query category.

**Parameters:**
- `response` (str): Raw response text
- `category` (str): Query category

**Returns:**
- `str`: Formatted response

#### `TextProcessor` Class

Core text processing functionality.

**Methods:**

##### `clean_text(text: str) -> str`
Clean and normalize input text.

##### `extract_keywords(text: str) -> List[str]`
Extract tax-related keywords from text.

##### `categorize_query(text: str) -> str`
Categorize the tax query based on content.

##### `extract_numbers(text: str) -> List[float]`
Extract numerical values from text.

##### `format_currency(amount: float) -> str`
Format amount as Pakistani Rupees.

##### `validate_query(text: str) -> Dict[str, Any]`
Validate and analyze the input query.

### 4. Error Handling (`utils/error_handler.py`)

#### `handle_error(error: Exception, error_type: str = "general", **kwargs) -> str`

Main error handling function.

**Parameters:**
- `error` (Exception): The exception that occurred
- `error_type` (str): Type of error ("api", "validation", "calculation", "general")
- `**kwargs`: Additional context parameters

**Returns:**
- `str`: User-friendly error message

**Example:**
```python
from utils.error_handler import handle_error

try:
    # Some operation that might fail
    result = risky_operation()
except Exception as e:
    error_msg = handle_error(e, "api", provider="huggingface")
    print(error_msg)
```

#### `log_interaction(user_input: str, response: str, response_time: float)`

Log user interaction for analytics.

**Parameters:**
- `user_input` (str): User's query
- `response` (str): System response
- `response_time` (float): Response time in seconds

#### `ErrorHandler` Class

Centralized error handling system.

**Methods:**

##### `handle_api_error(error: Exception, provider: str) -> str`
Handle API-related errors.

##### `handle_validation_error(error: Exception, user_input: str) -> str`
Handle input validation errors.

##### `handle_calculation_error(error: Exception, income: float) -> str`
Handle tax calculation errors.

##### `handle_general_error(error: Exception, context: str = "") -> str`
Handle general application errors.

## Integration Examples

### Basic Tax Query Processing

```python
from utils.llm_utils import get_llm_response
from utils.text_processing import process_query
from utils.error_handler import handle_error, log_interaction
import time

def process_tax_query(user_input: str) -> str:
    start_time = time.time()
    
    try:
        # Validate and process query
        analysis = process_query(user_input)
        
        if not analysis['valid']:
            return analysis['suggestion']
        
        # Get AI response
        response = get_llm_response(user_input)
        
        # Log interaction
        response_time = time.time() - start_time
        log_interaction(user_input, response, response_time)
        
        return response
        
    except Exception as e:
        return handle_error(e, "general", context="query_processing")
```

### Custom Tax Calculation

```python
from tax_data.pakistan_tax_data import PakistanTaxData
from utils.text_processing import TextProcessor

def calculate_custom_tax(income: float, deductions: float = 0) -> Dict[str, Any]:
    tax_data = PakistanTaxData()
    text_processor = TextProcessor()
    
    # Calculate base tax
    base_calculation = tax_data.calculate_income_tax(income)
    
    # Apply deductions
    taxable_income = max(0, income - deductions)
    final_calculation = tax_data.calculate_income_tax(taxable_income)
    
    return {
        'gross_income': income,
        'deductions': deductions,
        'taxable_income': taxable_income,
        'tax_before_deductions': base_calculation['total_tax'],
        'tax_after_deductions': final_calculation['total_tax'],
        'tax_saved': base_calculation['total_tax'] - final_calculation['total_tax'],
        'net_income': income - final_calculation['total_tax'],
        'formatted_net': text_processor.format_currency(income - final_calculation['total_tax'])
    }
```

### Adding New Tax Regime Support

```python
# Example: Adding Sales Tax support

class PakistanSalesTaxData:
    def __init__(self):
        self.standard_rate = 18.0
        self.reduced_rates = {
            'essential_items': 0.0,
            'reduced_rate_items': 5.0
        }
    
    def calculate_sales_tax(self, amount: float, category: str = 'standard') -> Dict[str, Any]:
        if category == 'essential_items':
            rate = self.reduced_rates['essential_items']
        elif category == 'reduced_rate_items':
            rate = self.reduced_rates['reduced_rate_items']
        else:
            rate = self.standard_rate
        
        tax_amount = amount * (rate / 100)
        total_amount = amount + tax_amount
        
        return {
            'base_amount': amount,
            'tax_rate': rate,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'category': category
        }

# Integration with existing system
def extend_llm_context_for_sales_tax():
    # Add sales tax context to LLM responses
    sales_tax_context = """
    Pakistan Sales Tax Information:
    - Standard rate: 18%
    - Essential items: 0%
    - Reduced rate items: 5%
    """
    return sales_tax_context
```

## Error Codes and Messages

### API Errors

| Code | Message | Description |
|------|---------|-------------|
| API_TIMEOUT | Request timed out | API call exceeded timeout limit |
| API_RATE_LIMIT | Rate limit exceeded | Too many API requests |
| API_AUTH_FAILED | Authentication failed | Invalid API key |
| API_UNAVAILABLE | Service unavailable | API service is down |

### Validation Errors

| Code | Message | Description |
|------|---------|-------------|
| QUERY_TOO_SHORT | Query too short | Input less than 3 characters |
| QUERY_TOO_LONG | Query too long | Input exceeds 500 characters |
| INVALID_INPUT | Invalid input format | Malformed input data |

### Calculation Errors

| Code | Message | Description |
|------|---------|-------------|
| INVALID_INCOME | Invalid income amount | Negative or invalid income value |
| CALCULATION_FAILED | Calculation failed | Error in tax calculation logic |

## Rate Limits and Quotas

### HuggingFace Inference API
- Free tier: 1,000 requests per month
- Rate limit: 10 requests per minute

### OpenRouter.ai
- Free tier: Varies by model
- Rate limit: Model-dependent

### OpenAI API
- Pay-per-use pricing
- Rate limit: Based on subscription tier

## Best Practices

### 1. Error Handling
Always wrap API calls in try-catch blocks and provide meaningful error messages to users.

### 2. Caching
Implement caching for frequently requested tax data to reduce API calls and improve performance.

### 3. Input Validation
Validate all user inputs before processing to prevent errors and security issues.

### 4. Logging
Log all interactions for debugging and analytics purposes.

### 5. Rate Limiting
Implement client-side rate limiting to stay within API quotas.

## Testing

### Unit Tests

```python
import pytest
from tax_data.pakistan_tax_data import get_tax_calculation

def test_tax_calculation():
    result = get_tax_calculation(1000000)
    assert result['total_tax'] == 10000  # 2.5% on 400,000
    assert result['effective_rate'] == 1.0

def test_zero_income():
    result = get_tax_calculation(0)
    assert result['total_tax'] == 0
    assert result['effective_rate'] == 0
```

### Integration Tests

```python
def test_full_query_processing():
    from utils.llm_utils import get_llm_response
    
    response = get_llm_response("What are the current tax rates?")
    assert "Tax Year 2024-25" in response
    assert "Rs. 600,000" in response
```

## Changelog

### Version 1.0.0
- Initial release with income tax support
- Multi-LLM provider integration
- Streamlit web interface
- Basic tax calculations

### Future Versions
- Sales tax support (v1.1.0)
- Corporate tax support (v1.2.0)
- Multilingual support (v2.0.0)
- Mobile app (v2.1.0)

## Support

For API-related questions or issues:
- GitHub Issues: [Create an issue](https://github.com/Ahmedbhatti001/TaxNova-Chatbot/issues)
- Email: ahmmedbhatti@gmail.com
- Documentation: Check the main README.md for general usage

