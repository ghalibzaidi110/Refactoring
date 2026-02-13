# Render Deployment Checklist

## Pre-Deployment

- [x] Push code to GitHub/GitLab repository
- [x] Ensure all dependencies are in requirements.txt
- [x] Create build.sh script
- [x] Create render.yaml configuration
- [x] Add runtime.txt for Python version

## Render Setup

1. **Create Web Service**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository

2. **Service Configuration**
   ```
   Name: refactorgpt
   Environment: Python
   Build Command: ./build.sh
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables** (Required)
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `GOOGLE_API_KEY` - (Optional) Your Google AI API key

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~2-5 minutes)

## Post-Deployment

- [ ] Check deployment logs for errors
- [ ] Visit your app URL (e.g., https://refactorgpt.onrender.com)
- [ ] Test the web UI
- [ ] Test the API endpoint: POST /refactor
- [ ] Test the health check: GET /health

## Troubleshooting

### Port Binding Issues
✅ **FIXED**: Start command now uses `$PORT` environment variable
- Render automatically provides the PORT variable
- App binds to 0.0.0.0:$PORT

### Build Failures
- Check build.sh has execute permissions (chmod +x build.sh)
- Verify requirements.txt is complete
- Check Python version in runtime.txt

### Import/Module Errors
- Ensure all imports use absolute paths (e.g., `from app.main import app`)
- Verify __init__.py files exist in all package directories

### API Key Issues
- Set OPENAI_API_KEY in Render environment variables
- Keys are not included in git (see .gitignore)
- Test without LLM first: set use_llm=false in requests

## Quick Test Commands

```bash
# Health check
curl https://your-app.onrender.com/health

# API test (without LLM)
curl -X POST https://your-app.onrender.com/refactor \
  -H "Content-Type: application/json" \
  -d '{"code": "def test():\n  print(1)", "use_llm": false}'

# API test (with LLM - requires API key)
curl -X POST https://your-app.onrender.com/refactor \
  -H "Content-Type: application/json" \
  -d '{"code": "def test():\n  print(1)", "use_llm": true}'
```

## Common Render URLs

- Dashboard: https://dashboard.render.com/
- Logs: Click on your service → "Logs" tab
- Environment: Click on your service → "Environment" tab
- Settings: Click on your service → "Settings" tab

## Free Tier Limitations

- Apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month of service time
- Consider upgrading for production use

## Success Indicators

✅ Build completes without errors
✅ Service shows "Live" status
✅ Health check returns {"status":"healthy","version":"1.0.0"}
✅ Web UI loads at root URL
✅ Code refactoring works (test with use_llm=false first)

---

**Need Help?**
- Check Render logs for detailed error messages
- Review the README.md deployment section
- Test locally first with: `./start.sh`
