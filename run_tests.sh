#!/bin/bash

# Simple script to run the test suite
# Usage: ./run_tests.sh

echo " Starting Zomato Cart Offer Tests- Narendra Kumar Thulasi - Assignment"
echo "Starting ...."

# Run tests
python3 -m pytest test_cart_offers.py -v

echo ""
echo "✅ Tests completed!"

