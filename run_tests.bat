@echo off
REM Simple script to run the test suite and generate HTML report
REM Assignment: Zomato Cart Offer Testing
REM Developer: Narendra Kumar
REM Usage: run_tests.bat

echo Starting Zomato Cart Offer Tests - Narendra Kumar Thulasi - Assignment
echo Starting ....
echo.

REM Check if pytest-html is installed
python -c "import pytest_html" 2>nul
if errorlevel 1 (
    echo Installing pytest-html for HTML report generation...
    pip install pytest-html
)

REM Run tests and generate HTML report
echo Running tests...
python -m pytest test_cart_offers.py --html=report.html --self-contained-html -v

echo.
echo Tests completed!
echo.
echo HTML report generated: report.html
echo Open report.html in your browser to view detailed results with response logs!
echo.
