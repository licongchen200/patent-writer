# 🐳 Docker Quick Start Guide

## Prerequisites
- Docker installed ([Download Docker Desktop](https://www.docker.com/products/docker-desktop))
- API Keys:
  - **Serper API** (free): https://serper.dev
  - **LLM**: Internal llm-proxy (default, no key needed) or OpenAI API

## 🚀 Quick Start (30 seconds)

### 1. Set up your API keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Serper API key
# LLM proxy is already configured for internal use!
# Use any text editor:
nano .env
# or
code .env
```

### 2. Build and run with Docker Compose
```bash
# Build and start the container
docker-compose up

# That's it! The system will start running.
```

## 💡 Alternative: Run with Docker directly

```bash
# Build the image
docker build -t patent-writer .

# Run with environment variables (using internal LLM proxy)
docker run -it \
  -e SERPER_API_KEY="your-serper-key" \
  -e OPENAI_API_BASE="http://llm-proxy.ceui.cnap.comcast.net" \
  -e OPENAI_API_KEY="dummy-key-not-needed" \
  -v $(pwd)/output:/app/output \
  patent-writer
```

## 📂 Output Files

Generated files will appear in the `output/` folder:
```bash
ls output/
# patent_application_iter_1.docx
# patent_data_iter_1.json
```

## 🔧 Advanced Usage

### Run in detached mode
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop the container
```bash
docker-compose down
```

### Rebuild after code changes
```bash
docker-compose up --build
```

### Run interactive shell in container
```bash
docker-compose run --rm patent-writer bash
```

### Run Python shell for debugging
```bash
# Access Python interpreter inside container
docker-compose run --rm patent-writer python
```

## 🎛️ Environment Variables

Edit `.env` file to configure:

```bash
# Required
SERPER_API_KEY=your-key-here

# Internal LLM Proxy (default, already set)
OPENAI_API_BASE=http://llm-proxy.ceui.cnap.comcast.net
OPENAI_API_KEY=dummy-key-not-needed

# Optional: Override to use external OpenAI instead
# OPENAI_API_BASE=https://api.openai.com/v1
# OPENAI_API_KEY=your-real-openai-key
# OPENAI_MODEL_NAME=gpt-4
```

## 🐛 Troubleshooting

### "Cannot connect to Docker daemon"
```bash
# Start Docker Desktop application
# Or on Linux:
sudo systemctl start docker
```

### "Permission denied" on output folder
```bash
# Fix permissions
chmod -R 755 output/
```

### "API key not found"
```bash
# Make sure .env file exists and has your keys
cat .env

# Rebuild container after .env changes
docker-compose down
docker-compose up --build
```

### Check if container is running
```bash
docker ps
# Should show 'patent-writer' container
```

### View container logs
```bash
docker logs patent-writer
```

### Remove all stopped containers and rebuild fresh
```bash
docker-compose down
docker system prune -f
docker-compose up --build
```

## 📊 Resource Usage

Typical resource requirements:
- **Disk**: ~2GB (Docker image)
- **Memory**: 1-2GB (during execution)
- **CPU**: 1-2 cores

## 🔄 Updating the Code

The `docker-compose.yml` mounts your local files, so:

1. Edit `main.py` locally
2. Save changes
3. Restart container:
   ```bash
   docker-compose restart
   ```

No rebuild needed for code changes!

## 🎯 Complete Example Workflow

```bash
# 1. Clone/navigate to project
cd /path/to/patent/crewai

# 2. Set up API keys
cp .env.example .env
echo "SERPER_API_KEY=sk-your-key" >> .env
echo "OPENAI_API_KEY=sk-your-key" >> .env

# 3. Run
docker-compose up

# 4. Wait for "HUMAN REVIEW REQUIRED" prompt
# 5. Review output/patent_application_iter_1.docx
# 6. Make decision: Approve (1) / Revise (2) / Exit (3)
# 7. Done!
```

## 📝 What Happens When You Run

1. **Docker builds** the image (first time only, ~2-5 minutes)
2. **Agents start working**:
   - Prior art research
   - Technical analysis
   - Novelty assessment
   - Claims drafting
   - Specification writing
   - Final review
3. **Files generated** in `output/` folder
4. **Prompt appears** for your review
5. **You decide**: Approve / Revise / Exit

## 🌟 Benefits of Docker Approach

✅ **No Python version issues**  
✅ **No dependency conflicts**  
✅ **Consistent environment**  
✅ **Easy to share**  
✅ **Clean uninstall** (just remove container)  
✅ **Works on Mac, Linux, Windows**  

## 🎉 You're Ready!

Just run:
```bash
docker-compose up
```

The patent writing system will start automatically! 🚀
