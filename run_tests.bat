@echo off
REM Simple script to run the test suite on Windows
REM Usage: run_tests.bat

echo Starting Zomato Cart Offer Tests...
echo.

REM Run tests
python -m pytest test_cart_offers.py -v

echo.
echo Tests completed!

