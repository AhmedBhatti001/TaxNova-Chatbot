# TaxNova Deployment Guide

## GitHub Repository Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Set repository name: `TaxNova-Chatbot`
4. Add description: "AI-powered chatbot for Pakistan Income Tax queries"
5. Make it public (recommended for portfolio)
6. Do NOT initialize with README (we already have one)
7. Click "Create repository"

### 2. Push Local Repository to GitHub

```bash
# Navigate to your project directory
cd TaxNova-Chatbot

# Add GitHub remote (replace with your GitHub username)
git remote add origin https://github.com/Ahmedbhatti001/TaxNova-Chatbot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Streamlit Community Cloud Deployment

### 1. Prerequisites

- GitHub repository with your TaxNova code
- Streamlit Community Cloud account (free)

### 2. Deploy to Streamlit Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `Ahmedbhatti001/TaxNova-Chatbot`
5. Set main file path: `app.py`
6. Choose a custom URL (optional): `taxnova-chatbot`
7. Click "Deploy!"

### 3. Configure Environment Variables

In the Streamlit Cloud dashboard:

1. Go to your app settings
2. Click on "Secrets"
3. Add your environment variables:

```toml
# Streamlit secrets format
LLM_PROVIDER = "huggingface"
HUGGINGFACE_API_KEY = "your_huggingface_api_key_here"
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
DEFAULT_MODEL = "microsoft/DialoGPT-medium"
MAX_TOKENS = 500
TEMPERATURE = 0.7
```

### 4. Update Code for Streamlit Cloud

If needed, update `utils/llm_utils.py` to use Streamlit secrets:

```python
import streamlit as st

# Replace os.getenv() calls with:
api_key = st.secrets.get("HUGGINGFACE_API_KEY", "")
```

## Alternative Deployment Options

### 1. Heroku Deployment

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### 2. Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t taxnova-chatbot .
docker run -p 8501:8501 taxnova-chatbot
```

### 3. Railway Deployment

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Railway will automatically deploy on git push

## Environment Variables Setup

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | Primary LLM provider | `huggingface` |
| `HUGGINGFACE_API_KEY` | HuggingFace API key | `hf_xxxxx` |
| `OPENROUTER_API_KEY` | OpenRouter API key | `sk-or-xxxxx` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-xxxxx` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_MODEL` | Default LLM model | `microsoft/DialoGPT-medium` |
| `MAX_TOKENS` | Maximum response tokens | `500` |
| `TEMPERATURE` | LLM temperature | `0.7` |

## API Keys Setup

### 1. HuggingFace API Key (Recommended)

1. Go to [HuggingFace](https://huggingface.co/)
2. Create an account and verify email
3. Go to Settings → Access Tokens
4. Create a new token with "Read" permissions
5. Copy the token (starts with `hf_`)

### 2. OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Go to Keys section
4. Create a new API key
5. Copy the key (starts with `sk-or-`)

### 3. OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and add payment method
3. Go to API Keys section
4. Create a new secret key
5. Copy the key (starts with `sk-`)

## Testing Deployment

### 1. Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export LLM_PROVIDER=huggingface
export HUGGINGFACE_API_KEY=your_key_here

# Run locally
streamlit run app.py
```

### 2. Production Testing

1. Test all major features:
   - Tax rate queries
   - Tax calculations
   - Error handling
   - Responsive design

2. Check logs for any errors
3. Verify API integrations work
4. Test on different devices

## Monitoring and Maintenance

### 1. Streamlit Cloud Monitoring

- Check app logs in Streamlit Cloud dashboard
- Monitor resource usage
- Set up alerts for downtime

### 2. API Usage Monitoring

- Monitor API key usage and limits
- Set up billing alerts if using paid APIs
- Rotate API keys periodically

### 3. Updates and Maintenance

```bash
# Update code
git add .
git commit -m "Update: description of changes"
git push origin main

# Streamlit Cloud will automatically redeploy
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Check requirements.txt includes all dependencies
2. **API Errors**: Verify API keys are correctly set
3. **Memory Issues**: Optimize code or upgrade hosting plan
4. **Slow Performance**: Implement caching with `@st.cache_data`

### Debug Mode

Add to your app for debugging:
```python
import streamlit as st

# Add debug info
if st.checkbox("Debug Mode"):
    st.write("Environment Variables:")
    st.write(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'Not set')}")
    st.write(f"API Key Set: {'Yes' if os.getenv('HUGGINGFACE_API_KEY') else 'No'}")
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Regularly rotate API keys**
4. **Monitor API usage** for unusual activity
5. **Keep dependencies updated**

## Support

For deployment issues:
- Check Streamlit Community Cloud documentation
- Review GitHub repository issues
- Contact: ahmmedbhatti@gmail.com

---

**Note**: This deployment guide assumes you have the necessary API keys and accounts set up. Free tier limitations may apply to some services.

