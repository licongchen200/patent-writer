# Quick Start Guide - Patent Writing System

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Get API Keys (2 min)
1. **Serper API** (free): https://serper.dev
   - Sign up → Get API key
2. **LLM Access**:
   - **Default**: Internal LLM Proxy (already configured, no key needed)
   - **Alternative**: OpenAI API: https://platform.openai.com/api-keys

### Step 3: Configure Environment (1 min)
```bash
# Option A: Create .env file
cat > .env << EOF
SERPER_API_KEY=your-serper-key-here
OPENAI_API_BASE=http://llm-proxy.ceui.cnap.comcast.net/v1
OPENAI_API_KEY=dummy-key-not-needed
EOF

# Option B: Export directly (temporary)
export SERPER_API_KEY="your-serper-key-here"
export OPENAI_API_BASE="http://llm-proxy.ceui.cnap.comcast.net/v1"
export OPENAI_API_KEY="dummy-key-not-needed"
```

### Step 4: Run the System (1 min)
```bash
# Run enhanced version
python main_enhanced.py
```

---

## 📝 What Happens Next?

1. **Agents start working** (5-15 minutes depending on LLM)
   - Prior art research
   - Technical analysis
   - Novelty assessment
   - Claims drafting
   - Specification writing
   - Final review

2. **Human review prompt appears**
   ```
   HUMAN REVIEW REQUIRED (Iteration 1)
   =====================================
   
   Options:
     1. Approve and finalize
     2. Request revisions
     3. Save draft and exit
   
   Your decision (1/2/3):
   ```

3. **Check output files**
   ```bash
   ls output/
   # patent_application_iter_1.docx
   # patent_data_iter_1.json
   ```

4. **Review the .docx file**
   - Open in Word/Google Docs
   - Check all sections
   - Verify claims and descriptions

5. **Make your decision**
   - ✅ Approve → Done!
   - 🔄 Revise → Provide feedback, system re-runs
   - 💾 Save → Keep draft, exit

---

## 💡 Quick Tips

### Customize Your Invention (BEFORE running)
Edit `main.py` at the bottom:

```python
invention_description = """
[Your invention description here]

Be specific about:
- What problem it solves
- How it works (technical details)
- What makes it unique
- Key components/features
"""
```

### Typical Run Time
- **With GPT-3.5-turbo**: 5-10 minutes
- **With GPT-4**: 15-25 minutes
- **With local Ollama**: 20-40 minutes

### Cost Estimates (per iteration)
- **Serper searches**: Free (up to 2,500/month)
- **Internal LLM Proxy**: Free (using Comcast infrastructure)
- **External OpenAI GPT-3.5**: ~$0.50-$1.00 (if not using internal proxy)
- **External OpenAI GPT-4**: ~$3.00-$5.00 (if not using internal proxy)
- **Local Ollama**: Free

---

## 🔧 Common Issues & Fixes

### Issue: "SERPER_API_KEY not found"
**Fix:**
```bash
export SERPER_API_KEY="your-actual-key"
```

### Issue: "Rate limit exceeded"
**Fix:** Wait a few minutes, or upgrade API plan

### Issue: Agents taking too long
**Fix:** Use faster model (GPT-3.5) or reduce verbosity:
```python
# In main.py, set verbose=False for agents
verbose=False
```

### Issue: Output files not found
**Check:**
```bash
ls -la output/
# Files should appear after completion
```

---

## 📚 What You Get

### Document Structure
✅ **Abstract** - 150-word summary  
✅ **Background** - Prior art and problems  
✅ **Summary** - Key innovations  
✅ **Detailed Description** - Full technical details  
✅ **Claims** - Legal protection scope  
✅ **Review** - Quality assessment  

### Files Generated
```
output/
├── patent_application_iter_1.docx  ← Main output (Word file)
└── patent_data_iter_1.json         ← Raw data (for reference)
```

---

## ⚠️ Critical Reminders

**BEFORE filing with USPTO:**
- [ ] Have patent attorney review
- [ ] Verify all prior art citations
- [ ] Ensure technical accuracy
- [ ] Check all claims are supported
- [ ] Consider provisional vs non-provisional
- [ ] Perform professional prior art search

**This generates DRAFTS only, not final filings!**

---

## 🎯 Next Steps After Generation

1. **Review Draft** - Read the entire .docx file carefully
2. **Check Claims** - Ensure they cover your invention properly
3. **Verify Prior Art** - Confirm citations are accurate
4. **Technical Review** - Have an engineer verify accuracy
5. **Legal Review** - Consult with a patent attorney
6. **Iterate if Needed** - Run again with feedback
7. **Professional Search** - Conduct thorough prior art search
8. **File Application** - Through attorney or USPTO directly

---

## 📞 Need Help?

- **CrewAI Docs**: https://docs.crewai.com
- **USPTO Resources**: https://www.uspto.gov
- **Patent Search**: https://patents.google.com

---

**Ready? Run this command:**
```bash
python main_enhanced.py
```

**Good luck with your patent! 🎉**
