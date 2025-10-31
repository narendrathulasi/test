# Zomato Cart Offer Testing Project

**Assignment by**: Narendra Kumar  
**Project**: Zomato Cart Offer - Automation Testing  
**Description**: Automated test suite for cart offer functionality using Python pytest framework and Flask mock service.

This project implements comprehensive test automation for Zomato's cart offer system, testing various scenarios including happy paths, negative cases, and corner cases.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### 2. Run All Tests

**Option A: Using the script (easiest)**
```bash
./run_tests.sh        # Linux/Mac
# or
run_tests.bat          # Windows
```

**Option B: Direct command**
```bash
python3 -m pytest test_cart_offers.py -v
```

> **Note**: Mock service automatically starts when running tests (no manual start needed)

## Test Results
- **Total Tests**: 51 test cases
- **Status**: All passing ✅
- **Coverage**: Happy paths, negative cases, and corner cases
- **Code Coverage**: ~83%

## Generating HTML Test Report

HTML reports provide detailed test execution results with response logs for debugging.

### How to Generate HTML Report After Running Tests

**After running `./run_tests.sh`, you have two options:**

#### Option 1: Use the HTML Report Script (Easiest - Runs Tests + Generates Report)
```bash
# This script runs the tests AND generates HTML report
./generate_html_report.sh
```

#### Option 2: Generate HTML Report Separately (If Tests Already Ran)
```bash
# If you already ran ./run_tests.sh, just generate the report:
python3 -m pytest test_cart_offers.py --html=report.html --self-contained-html -v
```

### Step-by-Step Guide to Generate HTML Report

#### Step 1: Install pytest-html (if not already installed)
```bash
pip install pytest-html
# or
pip3 install pytest-html
```

#### Step 2: Generate HTML Report

**Option A: Using the script (recommended - runs tests + generates report)**
```bash
./generate_html_report.sh        # Linux/Mac
```
This script will:
- ✅ Check and install pytest-html if needed
- ✅ Run all tests
- ✅ Generate HTML report with detailed logs

**Option B: Direct command (after running tests separately)**
```bash
# Simple HTML report
python3 -m pytest test_cart_offers.py --html=report.html --self-contained-html

# HTML report with code coverage
python3 -m pytest test_cart_offers.py --html=report.html --self-contained-html --cov=mock_service --cov-report=html
```

#### Step 3: View the Report
```bash
# Open report.html in your browser
open report.html        # Mac
xdg-open report.html    # Linux
start report.html       # Windows
# Or simply double-click report.html
```

### What's Included in HTML Report
- ✅ Test execution summary
- ✅ Pass/fail status for each test
- ✅ Execution time per test
- ✅ Detailed error messages and stack traces
- ✅ API request/response logs (for debugging)
- ✅ Environment information
- ✅ Code coverage (if included)

## Common Commands

### Run all tests
```bash
python3 -m pytest test_cart_offers.py -v
```

### Run with coverage report
```bash
python3 -m pytest test_cart_offers.py --cov=mock_service --cov-report=term-missing
```

### Generate HTML report (quick way)
```bash
./generate_html_report.sh
```

### Run specific test class
```bash
python3 -m pytest test_cart_offers.py::TestApplyOffer -v
```

### Run specific test
```bash
python3 -m pytest test_cart_offers.py::TestApplyOffer::test_apply_flat_amount_offer_p1_segment -v
```

### Run mock service standalone (optional)
```bash
python3 mock_service.py
# Service runs on http://localhost:5001
```

## Project Structure
```
project_luci/
├── api/                    # API client classes
├── test_data/              # Test data and constants
├── mock_service.py         # Flask mock service
├── test_cart_offers.py     # Test cases (51 tests)
├── conftest.py             # Pytest configuration
├── requirements.txt        # Dependencies
├── run_tests.sh           # Test execution script
├── generate_html_report.sh # HTML report generation script
└── report.html             # Generated HTML report (after running)
```

## API Endpoints

### Add Offer
```bash
POST /api/v1/offer
Request:
{
    "restaurant_id": 1,
    "offer_type": "FLATX",      # or "FLAT%"
    "offer_value": 10,
    "customer_segment": ["p1"]
}
Response:
{
    "response_msg": "success"
}
```

### Apply Offer to Cart
```bash
POST /api/v1/cart/apply_offer
Request:
{
    "cart_value": 200,
    "user_id": 1,
    "restaurant_id": 1
}
Response:
{
    "cart_value": 190
}
```

### Get User Segment
```bash
GET /api/v1/user_segment?user_id=1
Response:
{
    "segment": "p1"
}
```

## Test Coverage

### Happy Paths
- Adding offers (FLATX and FLAT% types)
- Applying offers to cart
- Multiple segments and restaurants
- User segment management

### Negative Cases
- Missing/empty fields
- Invalid data types
- Negative values
- Null values

### Corner Cases
- Zero values
- Very large/small values
- Percentage > 100%
- Floating point precision
- Cart value equals discount

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Notes

- Mock service runs automatically during tests (no manual start needed)
- Data is stored in memory and cleared between test runs
- Customer segments: `p1`, `p2`, `p3`
- Offer types: `FLATX` (flat amount off) or `FLAT%` (flat percentage off)
- HTML reports include API request/response logs for debugging
- All test responses are logged for easy troubleshooting

## Additional Documentation

For detailed test results and complete test case list, see:
- **TEST_RESULTS.md** - Complete test case documentation with response logs
- **PROJECT_STRUCTURE.md** - Architecture and code organization details
