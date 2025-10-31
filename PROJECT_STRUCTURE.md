# Project Structure Documentation

## Overview

This project is assignment for Lucidity test which does the functional test coverage of zomato cart offer. 

## Directory Structure

```
/
├── api/                          # API Client Classes
│   ├── __init__.py              # Module exports
│   └── cart_api.py              # CartAPI class for all API operations
│
├── test_data/                    # Test Data Module
│   ├── __init__.py              # Module exports
│   └── test_data.py             # Test data classes and constants
│
├── mock_service.py               # Flask mock service
├── test_cart_offers.py           # Pytest test cases
├── conftest.py                   # Pytest fixtures and configuration
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── TEST_RESULTS.md              # Test execution summary
└── PROJECT_STRUCTURE.md         # This file
```

## API Classes (`api/cart_api.py`)

### CartAPI Class

An API client that encapsulates all HTTP operations:

```python
class CartAPI:
    def __init__(base_url: str)
    def add_offer(restaurant_id, offer_type, offer_value, customer_segment)
    def apply_offer(cart_value, user_id, restaurant_id)
    def get_user_segment(user_id)
    def set_user_segment(user_id, segment)
    def health_check()
```

## Test Data Module (`test_data/test_data.py`)

### Data Classes

1. **OfferTestData**: Dataclass for offer creation
   - `restaurant_id`, `offer_type`, `offer_value`, `customer_segment`
   - `to_dict()` method for easy conversion

2. **CartTestData**: Dataclass for cart operations
   - `cart_value`, `user_id`, `restaurant_id`, `expected_cart_value`
   - `to_dict()` method for API requests

3. **UserSegmentTestData**: Dataclass for user segments
   - `user_id`, `segment`

### TestData Class

Contains all constants and helper methods:

#### Constants
- Restaurant IDs: `RESTAURANT_1`, `RESTAURANT_2`, etc.
- User IDs: `USER_1`, `USER_2`, etc.
- Segments: `SEGMENT_P1`, `SEGMENT_P2`, `SEGMENT_P3`
- Offer Types: `OFFER_TYPE_FLATX`, `OFFER_TYPE_FLAT_PERCENT`
- Offer Values: `OFFER_VALUE_10`, `OFFER_VALUE_15`, etc.
- Cart Values: `CART_VALUE_200`, `CART_VALUE_100_50`, etc.
- Expected Results: `EXPECTED_190`, `EXPECTED_180`, etc.

#### Helper Methods
- `get_valid_flatx_offer_p1()` - Pre-configured FLATX offer
- `get_valid_flat_percent_offer_p2()` - Pre-configured FLAT% offer
- `get_cart_apply_offer_p1()` - Pre-configured cart data
- `get_user_segment_p1()` - Pre-configured user segment
- And many more...

## Test Structure (`test_cart_offers.py`)

### Before Refactoring
- Direct `requests` calls scattered throughout tests
- Hard-coded values in test methods
- Difficult to maintain and reuse

### After Refactoring
- Clean use of `CartAPI` class
- Test data from centralized module
- Easy to read and maintain
- Reusable components

### Example Comparison

**Before:**
```python
def test_apply_offer(self, mock_server):
    response = requests.post(
        f'{BASE_URL}/api/v1/cart/apply_offer',
        json={
            'cart_value': 200,
            'user_id': 1,
            'restaurant_id': 1
        }
    )
    assert response.status_code == 200
```

**After:**
```python
def test_apply_offer(self, api_client: CartAPI):
    cart_data = TestData.get_cart_apply_offer_p1()
    response = api_client.apply_offer(
        cart_value=cart_data.cart_value,
        user_id=cart_data.user_id,
        restaurant_id=cart_data.restaurant_id
    )
    assert response['status_code'] == 200
    assert response['data']['cart_value'] == cart_data.expected_cart_value
```

## Benefits of Refactored Structure

1. **Maintainability**: Changes to API endpoints only need updates in `api/cart_api.py`
2. **Reusability**: API classes can be used across multiple test suites
3. **Readability**: Test code focuses on test logic, not API details
4. **Consistency**: All tests use the same API client and data structure
5. **Type Safety**: Dataclasses and type hints improve IDE support
6. **Testability**: Easy to mock API classes for unit testing
7. **Scalability**: Easy to add new API endpoints or test data

## Migration Guide

If you need to add new tests:

1. **Add API methods** in `api/cart_api.py`
2. **Add test data** in `test_data/test_data.py`
3. **Write test** using both in `test_cart_offers.py`

Example:
```python
# 1. API method already exists or add new one
response = api_client.apply_offer(...)

# 2. Use existing test data or create new
cart_data = TestData.get_cart_apply_offer_p1()

# 3. Write clean test
def test_new_scenario(self, api_client: CartAPI):
    # Setup
    offer_data = TestData.get_valid_flatx_offer_p1()
    api_client.add_offer(...)
    
    # Test
    response = api_client.apply_offer(...)
    
    # Assert
    assert response['status_code'] == 200
```

## Testing

All 21 tests pass successfully with the new structure:

```bash
python3 -m pytest test_cart_offers.py -v
# 21 passed in 0.12s
```

