# Patent Writing System with CrewAI

An AI-powered patent application generation system using CrewAI that creates comprehensive patent drafts with iterative refinement and human-in-the-loop approval.

## 🌟 Features

### ✅ Core Capabilities
- **6 Specialized AI Agents** working sequentially:
  - Prior Art Researcher (USPTO & Google Patents search)
  - Technical Analyzer
  - Novelty Assessor
  - Claims Writer
  - Description Writer
  - Patent Reviewer

### ✅ All Features Included
- **🔍 Built-in USPTO & Google Patents Search**: Custom tools for patent database research
- **📄 Document Export**: Generates professional .docx files with proper formatting
- **🔄 Iterative Refinement Loop**: Allows multiple revision cycles based on feedback
- **👤 Human-in-the-Loop**: Manual review and approval at each iteration
- **📊 JSON Data Export**: Structured data storage for each iteration

## 📋 Prerequisites

1. **Python 3.8+**
2. **Serper API Key** (for web search)
   - Sign up at: https://serper.dev
   - Free tier: 2,500 searches/month
3. **LLM Access** - One of the following:
   - **Internal LLM Proxy** (Comcast k8s) - Default, no API key needed
     - URL: `http://llm-proxy.ceui.cnap.comcast.net`
   - **OpenAI API** - For external use
     - Get key at: https://platform.openai.com/api-keys
   - **Anthropic Claude** - Alternative LLM
   - **Local Ollama** - For offline use

## 🚀 Installation

### 1. Clone or navigate to the project directory
```bash
cd /path/to/patent/crewai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Create .env file
cp .env.example .env

# Edit .env with your Serper API key
# For internal use, LLM proxy is already configured!
export SERPER_API_KEY="your-serper-api-key"

# The system uses internal llm-proxy by default:
# OPENAI_API_BASE=http://llm-proxy.ceui.cnap.comcast.net
# OPENAI_API_KEY=dummy-key-not-needed
```

## 📖 Usage

### Test LLM Connection (Optional)
```bash
# Verify internal LLM proxy is accessible
python test_llm_proxy.py
```

### Run the Patent Writer
```bash
python main.py
```

### Customize Your Invention Description

Edit the `invention_description` in the `if __name__ == "__main__":` section:

```python
invention_description = """
Your detailed invention description here.

Include:
- What it does
- How it works
- What problem it solves
- What makes it different from existing solutions
- Key technical features
- Novel aspects
"""
```

## 🔄 Iterative Refinement Workflow

The enhanced version supports iterative refinement:

1. **First Run**: System generates initial patent draft
2. **Human Review**: You review the generated .docx file
3. **Decision Point**:
   - **Approve**: Finalize the patent application
   - **Request Revisions**: Provide specific feedback
   - **Save & Exit**: Keep the draft for later
4. **Iteration**: If revisions requested, agents re-run with your feedback
5. **Repeat**: Up to 3 iterations (configurable)

## 📂 Output Files

Generated files are saved in the `output/` folder:

```
output/
├── patent_application_iter_1.docx   # Word document (Iteration 1)
├── patent_data_iter_1.json          # Raw data (Iteration 1)
├── patent_application_iter_2.docx   # Word document (Iteration 2)
└── ...
```

### Document Structure

The generated .docx file includes:
- **Abstract** (150 words max)
- **Field of the Invention**
- **Background of the Invention**
- **Prior Art Analysis**
- **Summary of the Invention**
- **Detailed Description**
- **Claims** (Independent & Dependent)
- **Review Comments**

## ⚙️ Configuration

### Adjust Maximum Iterations
```python
result = run_patent_generation(
    invention_description=invention_description,
    max_iterations=5  # Default is 3
)
```

### Switch LLM Providers

**Using Internal LLM Proxy (Default):**
```bash
export OPENAI_API_BASE="http://llm-proxy.ceui.cnap.comcast.net"
export OPENAI_API_KEY="dummy-key-not-needed"
```

**Using External OpenAI:**
```bash
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_API_KEY="sk-your-real-key"
export OPENAI_MODEL_NAME="gpt-4"
```

**Using Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

**Using Local Ollama:**
```bash
export OPENAI_API_BASE="http://localhost:11434"
export OPENAI_MODEL_NAME="llama2"
```

## ⚠️ Important Disclaimers

**This system generates DRAFT patent applications only.**

Before filing, you MUST:

- ✅ **Have a patent attorney review** the application
- ✅ **Verify all prior art citations** are accurate
- ✅ **Ensure technical accuracy** of all descriptions
- ✅ **Check claims** are properly supported
- ✅ **Consider provisional vs non-provisional** filing strategy
- ✅ **Review USPTO formal requirements** compliance
- ✅ **Perform professional prior art search**

**This tool does NOT provide legal advice.**

## 🛠️ Troubleshooting

### "SERPER_API_KEY not found"
```bash
# Set the environment variable
export SERPER_API_KEY="your-key-here"

# Or add to .env file
echo "SERPER_API_KEY=your-key-here" >> .env
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### CrewAI rate limits
- Use appropriate delays between API calls
- Consider using local LLMs (Ollama) for development
- Upgrade to paid LLM provider tiers if needed

## 📚 Additional Resources

- **CrewAI Documentation**: https://docs.crewai.com
- **USPTO Search**: https://www.uspto.gov/patents/search
- **Google Patents**: https://patents.google.com
- **Patent Drafting Guide**: https://www.uspto.gov/patent

## ✨ Key Features

| Feature | Status |
|---------|--------|
| USPTO & Google Patents specific search | ✅ Included |
| Professional .docx export | ✅ Included |
| Iterative refinement (up to N iterations) | ✅ Included |
| Interactive human approval | ✅ Included |
| Structured JSON data export | ✅ Included |
| Context-aware revision feedback | ✅ Included |

## 💡 Example Use Case

```python
# Describe your invention
invention = """
A machine learning system that predicts equipment failures
in manufacturing plants by analyzing vibration patterns,
temperature fluctuations, and historical maintenance data.

Novel aspects:
- Combines multiple sensor types with ML
- Real-time prediction with 95% accuracy
- Self-calibrating algorithm
- Cloud-based dashboard

Advantages:
- Reduces downtime by 40%
- Prevents catastrophic failures
- Lower maintenance costs
"""

# Run generation
run_patent_generation(invention, max_iterations=3)
```

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to enhance the system with:
- Additional agent types
- Better parsing of results
- USPTO API integration
- Drawing generation
- More sophisticated claim drafting

---

**Remember**: This generates DRAFTS only. Always consult with a qualified patent attorney before filing.
