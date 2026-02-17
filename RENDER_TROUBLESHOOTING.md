# 🚨 Render Deployment Troubleshooting

## Current Status: `https://mlopsdemo.onrender.com` - Not Responding

### 🔍 Immediate Diagnostic Steps:

1. **Check Render Dashboard:**
   - Go to [render.com dashboard](https://dashboard.render.com/)
   - Click on your "mlopsdemo" service
   - Check **"Logs"** tab for errors

2. **Look for Common Issues in Logs:**

#### ❌ **Build Failures:**
```
ERROR: Could not find src.models.iris_model
ModuleNotFoundError: No module named 'src'
pip install failed
```

#### ❌ **Runtime Failures:**
```
ImportError: cannot import name 'app' from 'src.api.app'
Port 10000 is already in use
Application startup failed
```

#### ✅ **Success Indicators:**
```
Model loaded successfully from models/iris_model.joblib
Uvicorn running on http://0.0.0.0:10000
Application startup complete
```

### 🛠️ **Fix Attempts (Choose One):**

#### **Option 1: Fixed render.yaml (Committed)**
```yaml
buildCommand: |
  pip install --upgrade pip
  pip install -r requirements-api.txt
  mkdir -p models
  cd /opt/render/project && python3 -m src.models.iris_model

startCommand: cd /opt/render/project && python3 -m uvicorn src.api.app:app --host 0.0.0.0 --port $PORT --workers 1
```

#### **Option 2: Alternative Configuration**
If Option 1 fails, replace `render.yaml` content with:
```yaml
services:
  - type: web
    name: iris-classification-api
    runtime: python3
    buildCommand: pip install -r requirements-api.txt && python3 -c "from src.models.iris_model import main; main()"
    startCommand: python3 -c "import os; os.chdir('/opt/render/project'); import uvicorn; from src.api.app import app; uvicorn.run(app, host='0.0.0.0', port=int(os.environ['PORT']))"
    envVars:
      - key: PYTHONPATH
        value: /opt/render/project
    plan: free
```

#### **Option 3: Simplified Approach**
Create a new file `main.py` in root:
```python
import os
import sys
sys.path.append('/opt/render/project')

if __name__ == "__main__":
    # Train model if not exists
    from src.models.iris_model import main as train_model
    train_model()

    # Start server
    import uvicorn
    from src.api.app import app
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 🚀 **Redeploy Steps:**

1. **Push fixes:**
   ```bash
   git add .
   git commit -m "fix: render deployment configuration"
   git push origin main
   ```

2. **Trigger redeploy in Render:**
   - Go to service dashboard
   - Click "Manual Deploy" → "Deploy latest commit"
   - Watch logs in real-time

### 🔧 **Manual Deployment Alternative:**

If `render.yaml` continues failing, set up manually:

1. **Create Web Service manually**
2. **Build Command:**
   ```bash
   pip install -r requirements-api.txt && python3 -m src.models.iris_model
   ```
3. **Start Command:**
   ```bash
   python3 -m uvicorn src.api.app:app --host 0.0.0.0 --port $PORT
   ```
4. **Environment Variables:**
   - `PYTHONPATH` = `/opt/render/project`

### 📞 **Test Commands After Fix:**

```bash
# Health check (should return JSON)
curl https://mlopsdemo.onrender.com/health

# API info
curl https://mlopsdemo.onrender.com/api

# Simple prediction
curl -X POST "https://mlopsdemo.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### 🎯 **Expected Working URL Structure:**

```
✅ https://mlopsdemo.onrender.com/          → Web interface
✅ https://mlopsdemo.onrender.com/health    → {"status": "healthy"}
✅ https://mlopsdemo.onrender.com/docs      → Swagger UI
✅ https://mlopsdemo.onrender.com/predict   → API endpoint
```

---

**Next Step:** Check Render logs and apply the appropriate fix above!