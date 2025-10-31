#!/bin/bash

# Simple script to run the test suite and generate HTML report
# Assignment: Zomato Cart Offer Testing
# Developer: Narendra Kumar
# Usage: ./run_tests.sh

echo " Starting Zomato Cart Offer Tests- Narendra Kumar Thulasi - Assignment"
echo "Starting ...."
echo ""

# Check if pytest-html is installed
python3 -c "import pytest_html" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing pytest-html for HTML report generation..."
    pip3 install pytest-html
fi

# Run tests and generate HTML report
echo "Running tests..."
python3 -m pytest test_cart_offers.py --html=report.html --self-contained-html -v

echo ""
echo "✅ Tests completed!"
echo ""
echo "📊 HTML report generated: report.html"
echo "📋 Open report.html in your browser to view detailed results with response logs!"
echo ""
