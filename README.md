# TaxNova: AI Chatbot for Pakistan Tax Queries

![TaxNova Logo](assets/taxnova-banner.png)

**TaxNova** is an intelligent AI-powered chatbot designed to assist users with Pakistan's Income Tax system. Built with Streamlit and integrated with multiple Large Language Model (LLM) providers, TaxNova provides instant, accurate answers to tax-related queries, making tax compliance more accessible for Pakistani taxpayers.

## 🌟 Project Overview

TaxNova addresses the complexity of Pakistan's tax system by providing an intuitive, conversational interface where users can ask questions about income tax rates, deductions, filing procedures, and calculations. The system combines structured tax data with AI-powered responses to deliver comprehensive and reliable tax guidance.

### Key Features

- **Intelligent Tax Assistance**: AI-powered responses for complex tax queries
- **Real-time Tax Calculations**: Instant calculation of income tax based on current slabs
- **Comprehensive Tax Information**: Coverage of rates, deductions, filing deadlines, and procedures
- **Multi-LLM Support**: Integration with HuggingFace, OpenRouter, and OpenAI APIs
- **Responsive Web Interface**: Modern, mobile-friendly Streamlit UI
- **Offline Fallback**: Structured responses when API services are unavailable
- **Extensible Architecture**: Modular design for easy expansion to other tax regimes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for LLM API access (optional for basic functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ahmedbhatti001/TaxNova-Chatbot.git
   cd TaxNova-Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the chatbot**
   Open your browser and navigate to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

TaxNova supports multiple LLM providers. Configure your preferred provider in the `.env` file:

```env
# LLM Provider Selection (huggingface, openrouter, openai, or local)
LLM_PROVIDER=huggingface

# API Keys (choose one based on your provider)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
DEFAULT_MODEL=microsoft/DialoGPT-medium
MAX_TOKENS=500
TEMPERATURE=0.7
```

### LLM Provider Setup

#### Option 1: HuggingFace Inference API (Recommended for Free Tier)

1. Create an account at [HuggingFace](https://huggingface.co/)
2. Generate an API token from your profile settings
3. Set `LLM_PROVIDER=huggingface` and `HUGGINGFACE_API_KEY=your_token`

#### Option 2: OpenRouter.ai (Free Access LLMs)

1. Sign up at [OpenRouter.ai](https://openrouter.ai/)
2. Get your API key from the dashboard
3. Set `LLM_PROVIDER=openrouter` and `OPENROUTER_API_KEY=your_key`

#### Option 3: OpenAI API

1. Create an account at [OpenAI](https://platform.openai.com/)
2. Generate an API key
3. Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY=your_key`

## 📁 Project Structure

```
TaxNova-Chatbot/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── llm_utils.py          # LLM provider integrations
│   ├── text_processing.py    # Text analysis and processing
│   └── error_handler.py      # Error handling utilities
├── tax_data/                  # Tax system data and calculations
│   ├── __init__.py
│   └── pakistan_tax_data.py  # Pakistan tax rules and calculations
├── assets/                    # Static assets (images, etc.)
├── docs/                      # Additional documentation
└── logs/                      # Application logs (created at runtime)
```

## 💡 Usage Examples

### Basic Tax Queries

- "What are the current income tax rates in Pakistan?"
- "When is the filing deadline for salaried individuals?"
- "What deductions can I claim on my tax return?"

### Tax Calculations

- "Calculate tax for income of 2,000,000"
- "How much tax do I owe on 1,500,000 annual income?"
- "What's my net income after tax on 3,000,000?"

### Specific Information

- "What is the withholding tax rate on bank interest?"
- "How do I file my tax return online?"
- "What documents do I need for tax filing?"

## 🏗️ Architecture

### Core Components

1. **Streamlit Frontend** (`app.py`)
   - User interface and chat management
   - Session state handling
   - Real-time response display

2. **LLM Integration** (`utils/llm_utils.py`)
   - Multi-provider LLM support
   - Intelligent query routing
   - Fallback response system

3. **Tax Data Engine** (`tax_data/pakistan_tax_data.py`)
   - Current tax slabs and rates
   - Tax calculation algorithms
   - Structured tax information

4. **Text Processing** (`utils/text_processing.py`)
   - Query categorization
   - Keyword extraction
   - Response formatting

5. **Error Handling** (`utils/error_handler.py`)
   - Robust error management
   - Logging and monitoring
   - Graceful degradation

### Data Flow

1. User submits query through Streamlit interface
2. Text processor analyzes and categorizes the query
3. System checks for structured data responses first
4. If needed, query is sent to configured LLM provider
5. Response is formatted and displayed to user
6. Interaction is logged for analytics

## 🔄 Extending to Other Tax Regimes

TaxNova is designed with extensibility in mind. To add support for additional tax types:

### 1. Create New Tax Data Module

```python
# tax_data/sales_tax_data.py
class PakistanSalesTaxData:
    def __init__(self):
        self.standard_rate = 18
        self.reduced_rates = {...}
        # Add sales tax specific data
```

### 2. Update Text Processing

```python
# utils/text_processing.py
self.tax_keywords = {
    'sales_tax': ['sales tax', 'gst', 'vat'],
    'corporate_tax': ['corporate', 'company tax'],
    # Add new categories
}
```

### 3. Extend LLM Context

```python
# utils/llm_utils.py
def _get_enhanced_tax_context(self, category: str) -> str:
    if category == "sales_tax":
        return self._get_sales_tax_context()
    # Add new tax regime contexts
```

### 4. Update UI Components

Add new sidebar sections and help text for the additional tax regimes in `app.py`.

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=utils --cov=tax_data tests/
```

### Manual Testing

1. **Basic Functionality**
   - Test chat interface responsiveness
   - Verify message history persistence
   - Check error handling for invalid inputs

2. **Tax Calculations**
   - Test various income levels
   - Verify calculation accuracy
   - Check edge cases (zero income, very high income)

3. **LLM Integration**
   - Test with different API providers
   - Verify fallback behavior
   - Check response quality and relevance

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Streamlit Community Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Configure environment variables in the Streamlit dashboard
4. Deploy with one click

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Production Considerations

- Set up proper logging and monitoring
- Configure rate limiting for API calls
- Implement user authentication if required
- Set up SSL/TLS for secure connections
- Monitor API usage and costs

## 🤝 Contributing

We welcome contributions to TaxNova! Here's how you can help:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Ensure all tests pass: `pytest`
5. Submit a pull request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include unit tests for new functionality
- Update documentation for any API changes
- Ensure backward compatibility

### Areas for Contribution

- Additional tax regime support (Sales Tax, Corporate Tax)
- Enhanced UI/UX improvements
- Performance optimizations
- Additional LLM provider integrations
- Multilingual support (Urdu, regional languages)
- Mobile app development

## 📊 Performance and Monitoring

### Metrics Tracking

TaxNova includes built-in logging and monitoring:

- Query response times
- API usage statistics
- Error rates and types
- User interaction patterns

### Performance Optimization

- Caching of frequently requested tax data
- Efficient query categorization
- Optimized LLM prompt engineering
- Lazy loading of heavy dependencies

## 🔒 Security and Privacy

### Data Protection

- No personal tax information is stored
- API keys are securely managed through environment variables
- All communications use HTTPS in production
- Session data is temporary and not persisted

### API Security

- Rate limiting to prevent abuse
- Input validation and sanitization
- Error messages don't expose sensitive information
- Secure handling of API credentials

## 📚 Additional Resources

### Pakistan Tax System References

- [Federal Board of Revenue (FBR)](https://fbr.gov.pk/)
- [Income Tax Ordinance 2001](https://fbr.gov.pk/categ/income-tax-ordinance-2001/50149)
- [IRIS Tax Portal](https://iris.fbr.gov.pk/)

### Technical Documentation

- [Streamlit Documentation](https://docs.streamlit.io/)
- [HuggingFace Inference API](https://huggingface.co/docs/api-inference/index)
- [OpenRouter API Documentation](https://openrouter.ai/docs)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors and Acknowledgments

**Author**: Ahmed Abubakar  
**Email**: ahmmedbhatti@gmail.com  
**GitHub**: [@Ahmedbhatti001](https://github.com/Ahmedbhatti001)

### Acknowledgments

- Federal Board of Revenue (FBR) for tax data and regulations
- Streamlit team for the excellent web framework
- HuggingFace for accessible AI model hosting
- Open source community for various dependencies

## 📞 Support and Contact

For questions, issues, or contributions:

- **GitHub Issues**: [Create an issue](https://github.com/Ahmedbhatti001/TaxNova-Chatbot/issues)
- **Email**: ahmmedbhatti@gmail.com
- **Documentation**: Check the `docs/` folder for detailed guides

---

**Disclaimer**: TaxNova provides general information about Pakistan's tax system. For specific tax advice, please consult with a qualified tax professional or visit the official FBR website. The authors are not responsible for any tax-related decisions made based on this tool's output.

