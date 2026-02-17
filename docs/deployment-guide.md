# Deployment Guide

This guide covers how to deploy the Iris Classification API to various cloud platforms.

## Quick Deploy Options

### 1. Render (Recommended - Free Tier)

**Why Render?**
- ✅ 750 hours free per month
- ✅ Automatic deployments from GitHub
- ✅ Built-in SSL certificates
- ✅ Easy setup with `render.yaml`

**Steps:**

1. **Fork/Clone this repository**
2. **Sign up at [render.com](https://render.com)**
3. **Connect your GitHub account**
4. **Create new Web Service:**
   - Repository: Select this repo
   - Branch: `main` or `chore/initial-setup`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements-api.txt && python3 -m src.models.iris_model`
   - Start Command: `python3 -m uvicorn src.api.app:app --host 0.0.0.0 --port $PORT`

5. **Deploy!** - Render will automatically use `render.yaml`

**Expected URL:** `https://iris-classification-api.onrender.com`

---

### 2. Railway

**Steps:**

1. **Sign up at [railway.app](https://railway.app)**
2. **New Project → Deploy from GitHub**
3. **Select this repository**
4. **Railway will auto-detect Python and use `railway.json`**
5. **Deploy automatically**

**Free tier:** $5 credit per month

---

### 3. Fly.io

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and setup:**
   ```bash
   flyctl auth login
   flyctl launch
   ```

3. **Deploy:**
   ```bash
   flyctl deploy
   ```

---

## Local Development

### Prerequisites

- Python 3.9+
- Git

### Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/mlopsdemo.git
   cd mlopsdemo
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-api.txt
   ```

4. **Train model:**
   ```bash
   python3 -m src.models.iris_model
   ```

5. **Start API server:**
   ```bash
   python3 -m uvicorn src.api.app:app --reload
   ```

6. **Test the API:**
   ```bash
   python3 test-api.py
   ```

7. **Visit:** `http://localhost:8000`

---

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t iris-api .

# Run container
docker run -p 8000:8000 iris-api
```

### Docker Compose

```yaml
version: '3.8'
services:
  iris-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | 8000 | No |
| `PYTHONPATH` | Python module path | Current dir | No |
| `WEB_CONCURRENCY` | Number of workers | 1 | No |

---

## CI/CD Integration

### GitHub Actions

The repository includes GitHub Actions workflows:

**CI Pipeline (`.github/workflows/ci.yml`):**
- ✅ Code quality checks (black, flake8, mypy)
- ✅ Unit tests (pytest)
- ✅ Model training and validation
- ✅ Security scanning

**Deployment Pipeline (`.github/workflows/model-deployment.yml`):**
- ✅ Automatic deployment to staging
- ✅ Manual deployment to production
- ✅ Health checks and validation

### Trigger Deployments

**Automatic:**
- Push to `main` branch → Deploy to staging
- Successful CI → Deploy staging

**Manual:**
- Go to GitHub Actions → "Model Deployment" → "Run workflow"
- Choose environment: staging or production

---

## Monitoring & Health Checks

### Health Check Endpoint

```bash
curl https://your-app.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Monitoring Tips

1. **Set up uptime monitoring:**
   - Use services like UptimeRobot, Pingdom
   - Monitor `/health` endpoint every 5 minutes

2. **Log monitoring:**
   - Check application logs in hosting platform
   - Monitor for error patterns

3. **Performance monitoring:**
   - Track response times
   - Monitor memory usage (important on free tiers)

---

## Troubleshooting

### Common Issues

**1. Model not loading:**
```
Solution: Check that models/ directory exists and contains iris_model.joblib
```

**2. Memory issues on free tier:**
```
Solution: Reduce model complexity or upgrade to paid tier
```

**3. Cold starts (Render):**
```
Issue: App sleeps after 15 minutes of inactivity
Solution: Use uptime monitoring to keep it warm, or upgrade plan
```

**4. Build failures:**
```
Check: requirements-api.txt has correct dependencies
Check: Python version compatibility (3.9+)
```

### Debug Commands

**Local debugging:**
```bash
# Check model file
ls -la models/

# Test model loading
python3 -c "from src.api.app import load_model; load_model()"

# Run tests
pytest tests/test_api.py -v

# Check API endpoints
python3 test-api.py
```

**Remote debugging:**
```bash
# Test deployed API
curl https://your-app.onrender.com/health
curl https://your-app.onrender.com/model/info
```

---

## Performance Optimization

### For Free Tiers

1. **Optimize model size:**
   - Use smaller Random Forest (fewer trees)
   - Consider simpler models for demo

2. **Memory management:**
   - Single worker (`WEB_CONCURRENCY=1`)
   - Lazy loading of dependencies

3. **Response optimization:**
   - Cache model metadata
   - Efficient JSON serialization

### For Production

1. **Scaling:**
   - Multiple workers
   - Load balancing
   - Database for model storage

2. **Caching:**
   - Redis for frequent predictions
   - CDN for static assets

3. **Monitoring:**
   - Application performance monitoring
   - Error tracking (Sentry)

---

## Security Considerations

### For Production Deployment

1. **API Security:**
   - Add authentication (API keys, OAuth)
   - Rate limiting
   - Input validation and sanitization

2. **Infrastructure:**
   - HTTPS only (enabled by default on most platforms)
   - Environment variable management
   - Network security groups

3. **Model Security:**
   - Model versioning
   - A/B testing for model updates
   - Rollback capabilities

### Current Demo Limitations

⚠️ **This is a demo API - Not production-ready:**
- No authentication required
- No rate limiting
- Public access to all endpoints
- No data persistence

---

## Cost Estimation

### Free Tiers

| Platform | Free Allowance | Limitations |
|----------|----------------|-------------|
| **Render** | 750 hours/month | Sleeps after 15min, 512MB RAM |
| **Railway** | $5 credit/month | Usage-based billing |
| **Fly.io** | 3 apps, 256MB RAM | Resource limits |
| **Heroku** | 550 hours/month | Sleeps after 30min |

### Paid Tiers (Starting prices)

| Platform | Starting Price | Benefits |
|----------|----------------|----------|
| **Render** | $7/month | Always-on, 512MB RAM |
| **Railway** | $5/month usage | Pay-as-you-go |
| **Fly.io** | $1.94/month | 256MB, more control |

---

## Next Steps

After successful deployment:

1. **✅ Test all endpoints**
2. **✅ Set up monitoring**
3. **✅ Configure custom domain (optional)**
4. **✅ Add authentication for production use**
5. **✅ Implement proper logging**
6. **✅ Set up CI/CD pipeline**
7. **✅ Add model versioning**

## Support

- **Documentation**: Check `/docs` endpoint on deployed API
- **Health Check**: Monitor `/health` endpoint
- **Logs**: Check platform-specific logging dashboards
- **Issues**: GitHub Issues for code-related problems