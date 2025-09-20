# Changelog

All notable changes to the Fraud Detection API project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.1] - 2025-09-20

### Added
- **New Carrier Support**: Added support for new Vietnamese carriers
  - **iTel (Indochina Telecom)**: 087 prefix
  - **Vietnamobile**: 092, 056, 058 prefixes  
  - **Wintel (VNPT subsidiary)**: 099 prefix
  - **VNPAY Sky**: 089 prefix
  - **Additional Vietnam prefixes**: 059, 090, 093, 095
- **Enhanced Database**: Updated phone headings database from 84 to 94 entries
- **Testing Script**: New `test_new_carriers.py` for validating new carrier prefixes

### Updated
- **Documentation**: Updated FRAUD_DETECTION_GUIDE.md with new carrier information
- **Phone Headings**: All new carriers marked as "safe" with LOW fraud risk
- **Database Statistics**: Updated to reflect 35 safe Vietnamese headings

## [3.1.0] - 2025-09-20

### Added
- **System Monitoring**: New `GET /` API status endpoint with real-time system metrics
- **Health Check**: New `GET /health` endpoint for monitoring database connectivity
- **System Metrics**: CPU and memory usage tracking with psutil integration
- **Uptime Monitoring**: Server uptime and performance metrics
- **Enhanced Testing**: New `test_api_status.py` script for comprehensive API testing
- **Batch Processing**: All endpoints now support batch operations for better performance
- **Error Handling**: Improved error handling with try-catch for missing dependencies

### Changed
- **API Status Response**: Enhanced with system information, endpoints list, and features status
- **Project Structure**: Updated README.md with correct file paths and new structure
- **Dependencies**: Added `psutil>=5.9.0` to requirements.txt for system monitoring
- **Documentation**: Updated all usage examples to reflect batch processing capabilities
- **Database Queries**: Fixed SQLAlchemy 2.0 compatibility with `text()` wrapper for raw SQL

### Fixed
- **Internal Server Error**: Fixed missing `psutil` dependency causing 500 errors
- **Database Health Check**: Fixed SQL syntax error in health check endpoint
- **Import Errors**: Added graceful fallback for missing psutil dependency
- **Path References**: Updated all documentation with correct file paths

### Technical Improvements
- **Performance**: Better response times with optimized system monitoring
- **Reliability**: Enhanced error handling and graceful degradation
- **Monitoring**: Real-time system health monitoring for production environments
- **Testing**: Comprehensive test coverage for all new features

## [3.0.0] - 2025-09-19

### Added
- **SMS Scam Detection**: Complete SMS spam/scam detection system
- **Banking Scam Detection**: Banking account fraud detection and reporting
- **Website Scam Detection**: Phishing and scam website detection
- **Batch Processing**: Support for processing multiple items in single requests
- **Enhanced API**: New endpoints for comprehensive fraud detection
- **Fuzzy Matching**: Advanced SMS content matching capabilities
- **Test Suite**: Comprehensive testing for all new features

### Changed
- **API Version**: Upgraded to v3.0.0 with new comprehensive fraud detection
- **Database Schema**: Added new tables for SMS, banking, and website scams
- **Response Format**: Enhanced response format with detailed analysis

## [2.0.0] - 2025-09-19

### Added
- New `POST /confirm-risky/` endpoint for confirming risky numbers
- Comprehensive project restructuring for better organization
- Complete README.md with installation and usage instructions
- API documentation in docs/API.md
- Setup and startup scripts in scripts/ directory
- .gitignore for proper version control
- Environment configuration example (env.example)
- Tests directory structure

### Changed
- Simplified API by removing unnecessary phone heading endpoints
- Updated Python dependencies for Python 3.13 compatibility
- Moved documentation files to docs/ directory
- Moved utility scripts to scripts/ directory
- Moved tests to tests/ directory
- Improved project structure for better maintainability

### Removed
- `GET /headings/` endpoint (unnecessary)
- `POST /headings/` endpoint (unnecessary)
- `GET /headings/{id}` endpoint (unnecessary)
- `GET /users/` endpoint (unnecessary)

### Fixed
- Python 3.13 compatibility issues with SQLAlchemy and Pydantic
- Package dependency conflicts
- Virtual environment setup issues

## [1.0.0] - 2025-09-18

### Added
- Initial FastAPI application
- Phone number fraud detection system
- PostgreSQL database integration
- SQLAlchemy ORM models
- Alembic database migrations
- Basic phone number analysis
- Region detection for phone numbers
- User and phone heading management endpoints
