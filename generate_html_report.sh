#!/bin/bash

# Script to generate HTML test report with detailed response logs
# Assignment: Zomato Cart Offer Testing
# Developer: Narendra Kumar
# Usage: ./generate_html_report.sh

echo "📊 Generating HTML Test Report with Response Logs..."
echo "Assignment: Zomato Cart Offer Testing - Narendra Kumar"
echo ""

# Check if pytest-html is installed
python3 -c "import pytest_html" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing pytest-html..."
    pip3 install pytest-html
fi

# Generate HTML report with detailed logging
echo "Running tests with detailed response logging..."
python3 -m pytest test_cart_offers.py --html=report.html --self-contained-html -v --log-cli-level=INFO

echo ""
echo "✅ HTML report generated: report.html"
echo "📋 The report includes:"
echo "   - All test results"
echo "   - API request/response logs"
echo "   - Status codes and response bodies"
echo "   - Error details (if any)"
echo ""
echo "Open report.html in your browser to view the results!"

