# Docker Deployment Guide for Arrow Backend

This guide covers running the Arrow Backend with Docker locally and deploying to Heroku.

## Prerequisites

- Docker and Docker Compose installed
- For Heroku deployment: Heroku CLI installed and account configured

## Local Development with Docker Compose

### 1. Setup Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` to set your MongoDB credentials and configuration:
- `MONGO_ROOT_PASSWORD`: Root password for MongoDB (change from default)
- `MONGO_DB_NAME`: Database name (default: arrow_backend)
- `ENVIRONMENT`: development, staging, or production
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

### 2. Build and Run

Start all services (MongoDB + Backend):

```bash
docker-compose up --build -d
```

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# MongoDB only
docker-compose logs -f mongodb
```

### 4. Check Health

Visit http://localhost:8000/health to verify the backend is running and connected to MongoDB.

API documentation is available at http://localhost:8000/docs

### 5. Stop Services

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (clean database)
docker-compose down -v
```

## Heroku Deployment

The Arrow Backend can be deployed to Heroku using either **Container Registry** (Docker-based) or **Python Buildpack** methods.

### Common Prerequisites

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set up MongoDB (choose one):
   
   **Option A: MongoDB Atlas (Recommended)**
   - Create a free cluster at https://www.mongodb.com/cloud/atlas
   - Get your connection string
   - Add Heroku's IP ranges to Atlas IP allowlist (or allow all IPs: 0.0.0.0/0)
   
   **Option B: Heroku Add-on**
   - Check available MongoDB add-ons in Heroku marketplace

4. Set required environment variables:
   ```bash
   heroku config:set MONGO_DB_CONNECTION_STRING="mongodb+srv://user:pass@cluster.mongodb.net/"
   heroku config:set MONGO_DB_NAME="arrow_backend"
   heroku config:set ENVIRONMENT="production"
   heroku config:set ALLOWED_ORIGINS="https://your-frontend.herokuapp.com"
   ```

### Method 1: Container Registry (Docker-based)

This method uses the Dockerfile and is ideal for consistent deployments.

1. Login to Heroku Container Registry:
   ```bash
   heroku container:login
   ```

2. Set stack to container:
   ```bash
   heroku stack:set container
   ```

3. Push and release the container:
   ```bash
   heroku container:push web
   heroku container:release web
   ```

4. Check logs:
   ```bash
   heroku logs --tail
   ```

**Note**: The `heroku.yml` file configures the container deployment and ensures the app binds to Heroku's `$PORT` variable.

### Method 2: Python Buildpack

This method uses Heroku's Python buildpack without Docker.

1. Ensure you're using the Python buildpack:
   ```bash
   heroku buildpacks:set heroku/python
   ```

2. Deploy via git push:
   ```bash
   git push heroku main
   ```

   Or if you're on a different branch:
   ```bash
   git push heroku your-branch:main
   ```

3. Check logs:
   ```bash
   heroku logs --tail
   ```

**Note**: The `Procfile` ensures the app binds to Heroku's `$PORT` variable.

## Troubleshooting Heroku Deployment

### Application Error / H10 Error

**Symptoms**: "Application error" page or H10 error in logs.

**Common causes and solutions**:

1. **Port binding issue**:
   - **Cause**: App not binding to Heroku's `$PORT` variable
   - **Solution**: Ensure using latest Procfile or heroku.yml from this repo
   - **Verify**: Check logs for "Started server process" and correct port

2. **Missing environment variables**:
   - **Cause**: MONGO_DB_CONNECTION_STRING or MONGO_DB_NAME not set
   - **Solution**: Set all required config vars:
     ```bash
     heroku config:set MONGO_DB_CONNECTION_STRING="your-connection-string"
     heroku config:set MONGO_DB_NAME="arrow_backend"
     heroku config:set ENVIRONMENT="production"
     ```
   - **Verify**: Run `heroku config` to list all variables

3. **Database connection failure**:
   - **Cause**: MongoDB not accessible from Heroku
   - **Solutions**:
     - If using Atlas: Add 0.0.0.0/0 to IP allowlist
     - Verify connection string format includes credentials
     - Check if TLS/SSL is required: add `?ssl=true` to connection string
   - **Verify**: Check logs for "Failed to initialize database" errors

4. **Missing dependencies**:
   - **Cause**: Some Python packages failed to install
   - **Solution**: Ensure requirements.txt includes all dependencies
   - **Verify**: Check build logs for pip install errors

5. **Memory/Timeout issues**:
   - **Cause**: App takes too long to start or uses too much memory
   - **Solution**: 
     - Upgrade dyno type: `heroku dyno:type hobby` or `standard-1x`
     - Optimize startup time
   - **Verify**: Check logs for R14 (Memory quota exceeded) or R10 (Boot timeout) errors

### Viewing Detailed Logs

```bash
# Tail all logs
heroku logs --tail

# Show last 500 lines
heroku logs -n 500

# Filter for errors
heroku logs --tail | grep -i error

# Show only app logs (not system)
heroku logs --source app --tail
```

### Testing the Health Endpoint

```bash
# Check if app is responding
curl https://your-app-name.herokuapp.com/health

# Expected response:
# {"status":"healthy","database":"connected","environment":"production"}
```

### Restarting the App

```bash
heroku restart
```

## Port Configuration Details

### How Port Binding Works

- **Local Docker**: Uses port 8000 (hardcoded fallback)
- **Heroku**: Uses `$PORT` environment variable (dynamically assigned by Heroku)

### Configuration Files

1. **Dockerfile**: 
   ```dockerfile
   CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
   Uses `$PORT` if set, otherwise defaults to 8000

2. **Procfile** (for buildpack):
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **heroku.yml** (for container):
   ```yaml
   run:
     web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

All three configurations ensure the app binds to Heroku's dynamically-assigned port.

## Health Checks

The application includes a `/health` endpoint that:
- Returns 200 OK if healthy and database is connected
- Returns 503 Service Unavailable if database is disconnected
- Can be used for monitoring and load balancer health checks

```bash
# Check health locally
curl http://localhost:8000/health

# Check health on Heroku
curl https://your-app-name.herokuapp.com/health
```

## Additional Resources

- [Heroku Python Documentation](https://devcenter.heroku.com/categories/python-support)
- [Heroku Container Registry](https://devcenter.heroku.com/articles/container-registry-and-runtime)
- [MongoDB Atlas Setup](https://www.mongodb.com/docs/atlas/getting-started/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## Security Notes

- Never commit `.env` file to git (already in `.gitignore`)
- Change default MongoDB password in production
- Set specific ALLOWED_ORIGINS in production (not "*")
- Use HTTPS for all production deployments
- Rotate MongoDB credentials regularly
- Use Heroku config vars for sensitive data (not .env files)
