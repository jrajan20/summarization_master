# Summarization Master

A Python-based intelligent web scraper and summarization tool that fetches website content and generates concise, snarky summaries using OpenAI's GPT models. The tool automatically handles both static and JavaScript-rendered websites using a smart hybrid approach.

## Features

- **Intelligent Web Scraping**: Automatically detects and handles JavaScript-rendered content
- **Hybrid Fetching Strategy**: Fast simple requests with Playwright fallback for dynamic sites
- **AI-Powered Summaries**: Generates concise summaries using OpenAI's GPT models
- **Batch Processing**: Summarize multiple websites at once
- **Markdown Output**: Clean, formatted summaries ready for display
- **Robust Error Handling**: Graceful fallbacks and timeout management

## Tech Stack

- **Python 3.11+**
- **Web Scraping**:
  - `requests` - Fast HTTP requests for static content
  - `BeautifulSoup4` - HTML parsing and content extraction
  - `playwright` - Browser automation for JavaScript-rendered sites
- **AI Integration**:
  - `openai` - GPT API integration for content summarization
- **Environment Management**:
  - `python-dotenv` - Secure API key management
- **Additional**: IPython, Jupyter support for interactive development

## Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd summarization_master
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -e .
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=sk-proj-your-api-key-here
```

## Usage

### Basic Example

```python
from scraper import fetch_website_contents
from summarize import summarize, display_summary

# Fetch website contents
content = fetch_website_contents("https://example.com")
print(content)

# Generate a summary
summary = summarize("https://example.com")
print(summary)

# Display formatted summary (in Jupyter)
display_summary("https://example.com")
```

### Batch Summarization

```python
from summarize import display_summaries

urls = [
    "https://edwarddonner.com",
    "https://www.openai.com",
    "https://www.google.com"
]

display_summaries(urls)
```

### Advanced Scraping

```python
from scraper import (
    fetch_website_contents_simple,  # Fast, no JS
    fetch_website_contents_js,      # Slower, handles JS
    fetch_website_contents,         # Smart hybrid approach
    fetch_website_links             # Extract all links
)

# Use simple method for static sites
content = fetch_website_contents_simple("https://example.com", timeout=10)

# Force JavaScript rendering
content = fetch_website_contents_js("https://spa-site.com", timeout=30000)

# Get all links from a page
links = fetch_website_links("https://example.com")
```

## How It Works

### Intelligent Scraping Strategy

1. **Fast First**: Attempts to fetch content using simple HTTP requests
2. **Smart Detection**: If content is suspiciously short (<500 chars), assumes JavaScript rendering
3. **Fallback**: Automatically uses Playwright to render JavaScript and extract content
4. **Content Extraction**: Removes scripts, styles, and irrelevant elements
5. **Truncation**: Returns first 2,000 characters for efficient summarization

### Summarization Pipeline

1. Fetches website content using the intelligent scraper
2. Sends content to OpenAI's GPT model with a custom system prompt
3. Receives a snarky, concise summary in markdown format
4. Optionally displays formatted output in Jupyter notebooks

## Configuration

### Custom System Prompt

Modify the `system_prompt` in `summarize.py` to change the summarization style:

```python
system_prompt = """
You are a helpful assistant that analyzes website contents
and provides professional summaries in bullet-point format.
Respond in markdown.
"""
```

### Timeout Settings

Adjust timeouts in scraper functions:

```python
# Simple requests timeout (seconds)
fetch_website_contents(url, timeout=30)

# Playwright timeout (milliseconds)
fetch_website_contents_js(url, timeout=60000)
```

## Project Structure

```
summarization_master/
├── scraper.py          # Web scraping utilities
├── summarize.py        # Summarization logic and OpenAI integration
├── pyproject.toml      # Project dependencies
├── .env               # API keys (create this)
└── README.md          # This file
```

## API Key Setup

1. Get your OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Create a `.env` file in the project root
3. Add your key: `OPENAI_API_KEY=sk-proj-your-key-here`
4. The script will validate your key format on startup

## Troubleshooting

- **API Key Issues**: Ensure your key starts with `sk-proj-` and has no extra whitespace
- **Playwright Errors**: Run `playwright install chromium` to install browser binaries
- **Timeout Errors**: Increase timeout values for slow-loading websites
- **JavaScript Sites**: The tool automatically handles JS, but you can force it with `fetch_website_contents_js()`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
