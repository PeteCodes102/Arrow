# Arrow Backend API

A production-ready FastAPI backend for managing trading alerts with strategy-based authentication using secret keys.

## Features

- **Trading Alert Management**: CRUD operations for trading alerts
- **Secret Key Authentication**: Secure strategy-based authentication system
- **Chart Generation**: Plotly-based chart generation with filtering
- **MongoDB Integration**: Async database operations using Beanie ODM
- **Production Ready**: Docker support, health checks, logging, and CORS configuration

## Architecture

### Project Structure

```
ArrowBackend/
├── core/                    # Core business logic
│   ├── constants.py        # Application constants
│   ├── deps.py             # Dependency injection
│   └── logic/              # Business logic modules
├── db/                      # Database configuration
│   └── base.py             # Database initialization
├── models/                  # Data models (Beanie Documents)
│   ├── alerts.py           # Alert document model
│   ├── secret_key.py       # Secret key document model
│   └── filters.py          # Filter models
├── routes/                  # API routes
│   ├── router.py           # Main aggregator router
│   ├── services.py         # Service orchestration layer
│   ├── data/               # Alert data endpoints
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   └── helpers.py
│   └── keys/               # Secret key endpoints
│       ├── router.py
│       ├── service.py
│       ├── repository.py
│       ├── schemas.py
│       └── helpers.py
├── tests/                   # Test suite
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker orchestration
└── .env.example            # Environment variables template
```

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ArrowBackend
   ```

2. **Set up environment**
   ```bash
   # Copy environment template
   copy .env.example .env
   
   # Edit .env with your configuration
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run MongoDB** (if not using Docker)
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

5. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Docker Deployment

1. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with production settings
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **View logs**
   ```bash
   docker-compose logs -f backend
   ```

4. **Stop services**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Health & Status

- `GET /` - Root endpoint
- `GET /health` - Health check with database status

### Alerts

- `GET /alerts/strategy_names` - Get all strategy names
- `POST /alerts/create/{secret_key}` - Create alert with secret key
- `POST /alerts/bind_key` - Bind new secret key to strategy

### Data (Alerts)

- `GET /data/` - List all alerts
- `GET /data/{item_id}` - Get specific alert
- `POST /data/` - Create new alert
- `PUT /data/{item_id}` - Update alert
- `DELETE /data/{item_id}` - Delete alert
- `POST /data/chart/filters` - Generate filtered chart
- `POST /data/{secret_key}` - Create alert via webhook (TradingView)

### Keys

- `GET /keys/{secret_key}` - Get strategy name by secret key

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# MongoDB Configuration
MONGO_DB_CONNECTION_STRING=mongodb://localhost:27017
MONGO_DB_NAME=arrow_backend

# Environment
ENVIRONMENT=development  # development, production, staging

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Logging
LOG_LEVEL=INFO
```

### Production Configuration

For production deployment:

1. Set `ENVIRONMENT=production`
2. Configure specific `ALLOWED_ORIGINS`
3. Use strong MongoDB credentials
4. Enable SSL/TLS for MongoDB connection
5. Set up proper logging aggregation
6. Configure reverse proxy (nginx/traefik)

## Security

### Secret Key Generation

Secret keys are generated using Python's `secrets` module with URL-safe tokens (32 bytes = ~43 characters).

### Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **CORS**: Restrict origins in production
3. **MongoDB**: Use authentication and SSL/TLS
4. **Rate Limiting**: Consider adding rate limiting middleware
5. **API Keys**: Rotate secret keys periodically

## TradingView Integration

To integrate with TradingView alerts:

1. **Create a secret key**
   ```bash
   POST /alerts/bind_key
   {
     "name": "My Strategy"
   }
   ```

2. **Use the returned secret key in TradingView webhook URL**
   ```
   http://your-domain.com/data/{secret_key}
   ```

3. **Configure TradingView alert message** (JSON format)
   ```json
   {
     "contract": "{{ticker}}",
     "trade_type": "buy",
     "quantity": 1,
     "price": {{close}}
   }
   ```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=routes --cov=models --cov=core

# Run specific test file
pytest tests/test_data_service.py
```

## Monitoring

### Health Checks

- Application: `GET /health`
- Database connectivity included in health check
- Docker health checks configured

### Logging

Logs are structured and include:
- Timestamp
- Logger name
- Log level
- Message

Configure log level via `LOG_LEVEL` environment variable.

## Performance Optimization

1. **Database Indexes**: Configured on frequently queried fields
   - `secret_key` (unique index)
   - `name` (index)
   - Alert compound indexes on contract, trade_type, etc.

2. **Connection Pooling**: Motor uses connection pooling by default

3. **Async Operations**: All database operations are async

4. **Caching**: Consider adding Redis for frequently accessed data

## Troubleshooting

### Database Connection Issues

```bash
# Check MongoDB is running
docker ps | grep mongo

# Check connection string
echo $MONGO_DB_CONNECTION_STRING

# Test connection
mongosh $MONGO_DB_CONNECTION_STRING
```

### CORS Issues

Ensure `ALLOWED_ORIGINS` includes your frontend URL and the backend is properly configured.

### Import Errors

```bash
# Verify all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

## License

[Your License Here]

## Support

For issues and questions:
- GitHub Issues: [Your Repo]
- Email: [Your Email]

