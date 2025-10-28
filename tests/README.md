# Tests for Mergington High School Activities API

This directory contains comprehensive test suites for the FastAPI application.

## Test Structure

- `test_app.py` - Main test suite covering all API endpoints and functionality

## Test Coverage

The test suite includes:

### Test Classes:
- **TestRootEndpoint** - Tests the root redirect functionality
- **TestGetActivities** - Tests retrieving all activities
- **TestSignupForActivity** - Tests student registration for activities
- **TestUnregisterFromActivity** - Tests participant removal from activities
- **TestEndToEndWorkflow** - Tests complete user workflows
- **TestErrorHandling** - Tests error cases and edge conditions

### Key Features Tested:
- ✅ Root path redirect to static files
- ✅ Activity data retrieval and structure validation
- ✅ Student signup functionality
- ✅ Duplicate registration prevention
- ✅ Participant unregistration
- ✅ Error handling for invalid activities/participants
- ✅ URL encoding support
- ✅ Complete signup/unregister workflows
- ✅ Edge cases and error conditions

## Running Tests

### Basic test run:
```bash
pytest tests/
```

### Verbose output:
```bash
pytest tests/ -v
```

### With coverage:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Generate HTML coverage report:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage Results

Current test coverage: **100%** - All code paths are tested!

## Dependencies

The following testing dependencies are required:
- `pytest` - Testing framework
- `httpx` - HTTP client for FastAPI testing
- `pytest-asyncio` - Async testing support
- `pytest-cov` - Coverage reporting

These are included in `requirements.txt` and will be installed automatically.