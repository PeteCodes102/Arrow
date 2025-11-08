# Testing Guide for Arrow Project

This document provides comprehensive information about testing the Arrow trading alerts management system.

## Table of Contents

1. [Overview](#overview)
2. [Backend Testing](#backend-testing)
3. [Frontend Testing](#frontend-testing)
4. [Running Tests](#running-tests)
5. [Test Coverage](#test-coverage)
6. [Writing Tests](#writing-tests)
7. [CI/CD Integration](#cicd-integration)

## Overview

The Arrow project uses comprehensive testing to ensure reliability and maintainability:

- **Backend**: Python tests using pytest, pytest-asyncio, and pytest-cov
- **Frontend**: React tests using Jest and React Testing Library
- **Coverage**: Automated coverage reporting with configurable thresholds
- **CI/CD**: GitHub Actions workflows for automated testing

## Backend Testing

### Test Framework

The backend uses:
- **pytest**: Main testing framework
- **pytest-asyncio**: For testing async functions
- **pytest-cov**: For code coverage reports
- **unittest.mock**: For mocking dependencies

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_core_constants.py   # Core constants tests
├── test_core_deps.py        # Dependency injection tests
├── test_data_*.py           # Data layer tests
├── test_keys_service.py     # Keys service tests
├── test_services_worker.py  # Service orchestration tests
├── test_alert_router.py     # Alert router tests
├── test_main.py             # Main app tests
├── test_models.py           # Model validation tests
├── test_logic.py            # Business logic tests
└── test_processing.py       # Data processing tests
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_keys_service.py

# Run tests matching a pattern
pytest -k "test_service"

# Run with coverage report
pytest --cov=routes --cov=models --cov=core --cov=db

# Generate HTML coverage report
pytest --cov=routes --cov=models --cov=core --cov=db --cov-report=html
# View report at htmlcov/index.html
```

### Test Configuration

Configuration is in `pytest.ini`:

```ini
[pytest]
testpaths = tests
asyncio_mode = auto
addopts = 
    -v
    --cov=routes
    --cov=models
    --cov=core
    --cov=db
    --cov-report=term-missing
    --cov-fail-under=40
```

### Backend Test Categories

#### Unit Tests
Fast tests with no external dependencies:
- `test_data_schemas.py` - Schema validation
- `test_data_service.py` - Service business logic
- `test_keys_service.py` - Keys service logic
- `test_services_worker.py` - Service orchestration
- `test_models.py` - Model validation

#### Integration Tests
Tests requiring database or external services:
- `test_data_router.py` - API endpoint integration
- `test_data_repository.py` - Database operations
- `test_main.py` - Full application tests

### Fixtures

Common fixtures in `conftest.py`:

```python
# Sample data fixtures
sample_alert_create
sample_alert_read
sample_alert_list
sample_alert_update

# Mock fixtures
mock_data_repository
mock_keys_repository
mock_db
mock_request
```

## Frontend Testing

### Test Framework

The frontend uses:
- **Jest**: Testing framework (via react-scripts)
- **React Testing Library**: Component testing utilities
- **@testing-library/user-event**: User interaction simulation

### Test Structure

```
alertfrontend/src/
├── App.test.tsx                      # Main app tests
├── components/
│   ├── Header.test.tsx              # Header component tests
│   ├── ChartPane.test.tsx           # Chart pane tests
│   └── FiltersPanel.test.tsx        # Filters panel tests
└── setupTests.ts                     # Test configuration
```

### Running Frontend Tests

```bash
cd alertfrontend

# Run all tests
npm test

# Run tests in CI mode (no watch)
npm test -- --watchAll=false

# Run with coverage
npm test -- --watchAll=false --coverage

# Run specific test file
npm test -- Header.test.tsx

# Update snapshots (if using)
npm test -- -u
```

### Frontend Test Configuration

Configuration in `jest.config.js`:

```javascript
module.exports = {
  preset: 'react-scripts',
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    'node_modules/(?!(axios)/)',
  ],
  coverageThresholds: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50,
    },
  },
};
```

## Test Coverage

### Current Coverage Status

**Backend Coverage: ~43%**
- High coverage (>90%): Services, routers, schemas, models
- Medium coverage (40-70%): Business logic, utilities
- Low coverage (<40%): Repositories (require database), core logic

**Frontend Coverage: In Progress**
- Component tests: Header, ChartPane, FiltersPanel
- App integration test
- Additional tests needed for API clients and chart components

### Coverage Thresholds

- **Backend**: Minimum 40% overall (configured in pytest.ini)
- **Frontend**: Minimum 50% per category (configured in jest.config.js)

### Viewing Coverage Reports

**Backend:**
```bash
# Generate and view HTML report
pytest --cov=routes --cov=models --cov=core --cov=db --cov-report=html
open htmlcov/index.html  # or xdg-open on Linux
```

**Frontend:**
```bash
cd alertfrontend
npm test -- --watchAll=false --coverage
open coverage/lcov-report/index.html
```

## Writing Tests

### Backend Test Example

```python
# tests/test_my_service.py
import pytest
from unittest.mock import AsyncMock
from routes.my_module.service import MyService
from routes.my_module.schemas import MyCreate, MyRead


@pytest.mark.asyncio
async def test_my_service_creates_item():
    """Test that service creates an item successfully."""
    # Arrange
    repo = AsyncMock()
    service = MyService(repo)
    payload = MyCreate(name="Test")
    expected = MyRead(id="123", name="Test")
    repo.create.return_value = expected
    
    # Act
    result = await service.create(payload)
    
    # Assert
    assert result.name == "Test"
    repo.create.assert_called_once()
```

### Frontend Test Example

```typescript
// src/components/MyComponent.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  test('renders with title', () => {
    render(<MyComponent title="Hello" />);
    expect(screen.getByText(/Hello/i)).toBeInTheDocument();
  });

  test('handles button click', async () => {
    const mockOnClick = jest.fn();
    render(<MyComponent onClick={mockOnClick} />);
    
    await userEvent.click(screen.getByRole('button'));
    
    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Best Practices

1. **Arrange-Act-Assert Pattern**: Structure tests clearly
2. **Descriptive Names**: Use clear test function names
3. **Single Responsibility**: One assertion per test when possible
4. **Mock External Dependencies**: Isolate units under test
5. **Test Edge Cases**: Include error handling and boundary conditions
6. **Use Fixtures**: Share common test data via fixtures
7. **Async/Await**: Properly handle async operations
8. **Clean Up**: Ensure mocks are reset between tests

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Push to main/master branches
- Pull requests to main/master branches

### Workflow Configuration

See `.github/workflows/python-tests.yml`:

- **Backend Tests**: Run on Python 3.11, 3.12, 3.13
- **Frontend Tests**: Run on Node 18, 20
- **Coverage Upload**: Coverage reports uploaded to Codecov

### Running Tests Locally Before Push

```bash
# Backend
pytest -v

# Frontend
cd alertfrontend && npm test -- --watchAll=false

# Both with coverage
pytest --cov=routes --cov=models --cov=core --cov=db
cd alertfrontend && npm test -- --watchAll=false --coverage
```

## Continuous Improvement

### Adding New Tests

When adding new features:
1. Write tests for new code (TDD approach recommended)
2. Ensure tests pass locally
3. Verify coverage meets thresholds
4. Update this documentation if needed

### Maintaining Tests

- Keep tests up to date with code changes
- Refactor tests when refactoring code
- Review and update fixtures as schemas evolve
- Monitor coverage trends to identify gaps

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure `PYTHONPATH` includes project root
- Check module imports match file structure

**Async Test Failures:**
- Use `@pytest.mark.asyncio` decorator
- Properly await async functions

**Mock Not Working:**
- Verify mock target path is correct
- Use `AsyncMock` for async functions
- Check mock is configured before use

**Coverage Too Low:**
- Add tests for uncovered code paths
- Check for untested edge cases
- Review coverage report for specific gaps

### Getting Help

- Check test output for specific error messages
- Review similar existing tests for patterns
- Consult pytest/Jest documentation
- Ask team members for assistance

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Jest documentation](https://jestjs.io/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
