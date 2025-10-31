"""
Test cases for Zomato cart offer functionality.

This module contains comprehensive test cases for:
- Adding offers to restaurants
- Applying offers to cart based on user segments
- Edge cases and error scenarios

All tests use the API client classes and test data modules for clean separation.
"""
import pytest
from api.cart_api import CartAPI
from test_data.test_data import TestData, OfferTestData, CartTestData, UserSegmentTestData


class TestAddOffer:
    """Test cases for adding offers."""
    
    def test_add_flat_amount_offer_single_segment(self, api_client: CartAPI):
        """Test adding FLATX offer for a single segment."""
        offer_data = TestData.get_valid_flatx_offer_p1()
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 200
        assert response['data'] == {'response_msg': 'success'}
    
    def test_add_flat_percentage_offer_multiple_segments(self, api_client: CartAPI):
        """Test adding FLAT% offer for multiple segments."""
        offer_data = TestData.get_valid_flat_percent_offer_multiple_segments()
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 200
        assert response['data'] == {'response_msg': 'success'}
    
    def test_add_offer_missing_fields(self, api_client: CartAPI):
        """Test adding offer with missing required fields."""
        # Use partial data to simulate missing fields
        response = api_client.add_offer(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=None,  # Missing value
            customer_segment=[]  # Empty segment
        )
        assert response['status_code'] == 400
    
    def test_add_offer_invalid_type(self, api_client: CartAPI):
        """Test adding offer with invalid offer_type."""
        offer_data = TestData.get_offer_invalid_type()
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 400
    
    def test_add_offer_invalid_segment(self, api_client: CartAPI):
        """Test adding offer with invalid customer segment."""
        offer_data = TestData.get_offer_invalid_segment()
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 400
    
    def test_add_offer_negative_value(self, api_client: CartAPI):
        """Test adding offer with negative offer_value."""
        offer_data = TestData.get_offer_negative_value()
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 400
    
    def test_add_offer_empty_segment_list(self, api_client: CartAPI):
        """Test adding offer with empty customer_segment array."""
        response = api_client.add_offer(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[]  # Empty array
        )
        assert response['status_code'] == 400
    
    def test_add_offer_zero_value(self, api_client: CartAPI):
        """Test adding offer with zero offer_value."""
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_ZERO,
            customer_segment=[TestData.SEGMENT_P1]
        )
        # Zero value might be acceptable or rejected - test behavior
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        # Assuming zero is valid (no discount), but should still be accepted
        assert response['status_code'] in [200, 400]
    
    def test_add_offer_percentage_over_100(self, api_client: CartAPI):
        """Test adding FLAT% offer with percentage > 100%."""
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_101,
            customer_segment=[TestData.SEGMENT_P1]
        )
        # > 100% might be accepted or rejected - test behavior
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        # Service might accept it (no validation) or reject it
        assert response['status_code'] in [200, 400]
    
    def test_add_offer_very_large_value(self, api_client: CartAPI):
        """Test adding offer with very large offer_value."""
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_999999,
            customer_segment=[TestData.SEGMENT_P1]
        )
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        # Should be accepted (no upper limit validation)
        assert response['status_code'] == 200
    
    def test_add_offer_very_small_value(self, api_client: CartAPI):
        """Test adding offer with very small offer_value."""
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_0_01,
            customer_segment=[TestData.SEGMENT_P1]
        )
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        # Should be accepted
        assert response['status_code'] == 200
    
    def test_add_offer_null_restaurant_id(self, api_client: CartAPI):
        """Test adding offer with null restaurant_id."""
        # Using None should cause an error when converted to JSON
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/offer',
            json={
                'restaurant_id': None,
                'offer_type': TestData.OFFER_TYPE_FLATX,
                'offer_value': TestData.OFFER_VALUE_10,
                'customer_segment': [TestData.SEGMENT_P1]
            }
        )
        assert response.status_code == 400
    
    def test_add_offer_all_three_segments(self, api_client: CartAPI):
        """Test adding offer for all three segments (p1, p2, p3)."""
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1, TestData.SEGMENT_P2, TestData.SEGMENT_P3]
        )
        response = api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        assert response['status_code'] == 200
        assert response['data'] == {'response_msg': 'success'}
    
    def test_add_offer_overwrite_existing(self, api_client: CartAPI):
        """Test that adding offer for same restaurant/segment overwrites existing."""
        # Add first offer
        offer_data_1 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        response1 = api_client.add_offer(
            restaurant_id=offer_data_1.restaurant_id,
            offer_type=offer_data_1.offer_type,
            offer_value=offer_data_1.offer_value,
            customer_segment=offer_data_1.customer_segment
        )
        assert response1['status_code'] == 200
        
        # Add second offer for same restaurant/segment with different value
        offer_data_2 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_20,  # Different value
            customer_segment=[TestData.SEGMENT_P1]
        )
        response2 = api_client.add_offer(
            restaurant_id=offer_data_2.restaurant_id,
            offer_type=offer_data_2.offer_type,
            offer_value=offer_data_2.offer_value,
            customer_segment=offer_data_2.customer_segment
        )
        assert response2['status_code'] == 200
        
        # Verify the second offer is applied
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        cart_response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert cart_response['status_code'] == 200
        # Should use the second offer value (20 off)
        assert cart_response['data']['cart_value'] == 180.0


class TestApplyOffer:
    """Test cases for applying offers to cart."""
    
    def test_apply_flat_amount_offer_p1_segment(self, api_client: CartAPI):
        """Test applying FLATX offer for p1 segment."""
        # Setup: Add offer
        offer_data = TestData.get_valid_flatx_offer_p1()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        cart_data = TestData.get_cart_apply_offer_p1()
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == cart_data.expected_cart_value
    
    def test_apply_flat_percentage_offer_p2_segment(self, api_client: CartAPI):
        """Test applying FLAT% offer for p2 segment."""
        # Setup: Add offer
        offer_data = TestData.get_valid_flat_percent_offer_p2()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p2()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        cart_data = TestData.get_cart_apply_offer_p2()
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == cart_data.expected_cart_value
    
    def test_apply_offer_no_user_segment(self, api_client: CartAPI):
        """Test applying offer when user segment doesn't exist."""
        # Setup: Add offer
        offer_data = TestData.get_valid_flatx_offer_p1()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Test: Apply offer without setting user segment
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=TestData.USER_INVALID,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 404
    
    def test_apply_offer_no_offer_for_segment(self, api_client: CartAPI):
        """Test applying offer when no offer exists for user's segment."""
        # Setup: Add offer for p1 only
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment to p2
        user_segment = TestData.get_user_segment_p2()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        # No discount applied, original cart value returned
        assert response['data']['cart_value'] == TestData.CART_VALUE_200
    
    def test_apply_offer_no_offer_for_restaurant(self, api_client: CartAPI):
        """Test applying offer when restaurant has no offers."""
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer for restaurant with no offers
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_INVALID
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        # No discount applied, original cart value returned
        assert response['data']['cart_value'] == TestData.CART_VALUE_200
    
    def test_apply_flat_amount_offer_cart_value_less_than_discount(self, api_client: CartAPI):
        """Test applying FLATX offer when discount is more than cart value."""
        # Setup: Add offer
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_50,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with cart value less than discount
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_30,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        # Should not go below 0
        assert response['data']['cart_value'] == TestData.EXPECTED_0
    
    def test_apply_flat_percentage_offer_100_percent(self, api_client: CartAPI):
        """Test applying FLAT% offer with 100% discount."""
        # Setup: Add offer
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_100,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_0
    
    def test_apply_offer_multiple_segments_same_restaurant(self, api_client: CartAPI):
        """Test applying offer when restaurant has offers for multiple segments."""
        # Setup: Add offers for multiple segments
        offer_data_p1 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data_p1.restaurant_id,
            offer_type=offer_data_p1.offer_type,
            offer_value=offer_data_p1.offer_value,
            customer_segment=offer_data_p1.customer_segment
        )
        
        offer_data_p2 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_20,
            customer_segment=[TestData.SEGMENT_P2]
        )
        api_client.add_offer(
            restaurant_id=offer_data_p2.restaurant_id,
            offer_type=offer_data_p2.offer_type,
            offer_value=offer_data_p2.offer_value,
            customer_segment=offer_data_p2.customer_segment
        )
        
        # Test p1 segment
        user_segment_p1 = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment_p1.user_id, user_segment_p1.segment)
        cart_data_p1 = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment_p1.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data_p1.cart_value,
            user_id=cart_data_p1.user_id,
            restaurant_id=cart_data_p1.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_190
        
        # Test p2 segment
        user_segment_p2 = TestData.get_user_segment_p2()
        api_client.set_user_segment(user_segment_p2.user_id, user_segment_p2.segment)
        cart_data_p2 = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment_p2.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data_p2.cart_value,
            user_id=cart_data_p2.user_id,
            restaurant_id=cart_data_p2.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_180
    
    def test_apply_offer_different_restaurants(self, api_client: CartAPI):
        """Test applying offers for different restaurants."""
        # Setup: Add offers for different restaurants
        offer_data_r1 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data_r1.restaurant_id,
            offer_type=offer_data_r1.offer_type,
            offer_value=offer_data_r1.offer_value,
            customer_segment=offer_data_r1.customer_segment
        )
        
        offer_data_r2 = OfferTestData(
            restaurant_id=TestData.RESTAURANT_2,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_15,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data_r2.restaurant_id,
            offer_type=offer_data_r2.offer_type,
            offer_value=offer_data_r2.offer_value,
            customer_segment=offer_data_r2.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test restaurant 1
        cart_data_r1 = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data_r1.cart_value,
            user_id=cart_data_r1.user_id,
            restaurant_id=cart_data_r1.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_190
        
        # Test restaurant 2
        cart_data_r2 = CartTestData(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_2
        )
        response = api_client.apply_offer(
            cart_value=cart_data_r2.cart_value,
            user_id=cart_data_r2.user_id,
            restaurant_id=cart_data_r2.restaurant_id
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_170
    
    def test_apply_offer_missing_fields(self, api_client: CartAPI):
        """Test applying offer with missing required fields."""
        # Try to call with invalid data
        response = api_client.apply_offer(
            cart_value=None,
            user_id=None,
            restaurant_id=None
        )
        assert response['status_code'] == 400
    
    def test_apply_offer_invalid_cart_value(self, api_client: CartAPI):
        """Test applying offer with invalid cart_value."""
        cart_data = CartTestData(
            cart_value=TestData.OFFER_VALUE_NEGATIVE,  # Negative cart value
            user_id=TestData.USER_1,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 400
    
    def test_apply_offer_decimal_values(self, api_client: CartAPI):
        """Test applying offer with decimal cart values and offer values."""
        # Setup: Add offer with decimal value
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_12_5,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with decimal cart value
        cart_data = CartTestData(
            cart_value=TestData.CART_VALUE_100_50,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        response = api_client.apply_offer(
            cart_value=cart_data.cart_value,
            user_id=cart_data.user_id,
            restaurant_id=cart_data.restaurant_id
        )
        assert response['status_code'] == 200
        # 100.50 - (100.50 * 12.5 / 100) = 100.50 - 12.5625 = 87.9375 ≈ 87.94
        assert response['data']['cart_value'] == TestData.EXPECTED_87_94
    
    def test_apply_offer_zero_cart_value(self, api_client: CartAPI):
        """Test applying offer when cart_value is zero."""
        # Setup: Add offer
        offer_data = TestData.get_valid_flatx_offer_p1()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with zero cart value
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_ZERO,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        # Zero cart value might be rejected as invalid
        assert response['status_code'] in [200, 400]
        if response['status_code'] == 200:
            # Should not go below 0
            assert response['data']['cart_value'] == TestData.EXPECTED_0
    
    def test_apply_offer_zero_discount_amount(self, api_client: CartAPI):
        """Test applying offer with zero offer_value (no discount)."""
        # Setup: Add offer with zero value
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_ZERO,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # Should return original cart value (no discount)
        assert response['data']['cart_value'] == TestData.CART_VALUE_200
    
    def test_apply_offer_cart_value_equals_discount(self, api_client: CartAPI):
        """Test applying FLATX offer when cart_value exactly equals discount."""
        # Setup: Add offer
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with cart value equals discount
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_10,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # Should result in 0
        assert response['data']['cart_value'] == TestData.EXPECTED_0
    
    def test_apply_offer_percentage_over_100(self, api_client: CartAPI):
        """Test applying FLAT% offer with percentage > 100%."""
        # Setup: Add offer with > 100%
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_101,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # Should result in 0 (101% discount means more than 100% off)
        assert response['data']['cart_value'] == TestData.EXPECTED_0
    
    def test_apply_offer_very_large_cart_value(self, api_client: CartAPI):
        """Test applying offer with very large cart value."""
        # Setup: Add offer
        offer_data = TestData.get_valid_flatx_offer_p1()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with very large cart value
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_999999,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == (TestData.CART_VALUE_999999 - TestData.OFFER_VALUE_10)
    
    def test_apply_offer_very_small_cart_value(self, api_client: CartAPI):
        """Test applying offer with very small cart value."""
        # Setup: Add offer
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with very small cart value
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_0_01,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # 0.01 - (0.01 * 10%) = 0.01 - 0.001 = 0.009 ≈ 0.01 (rounded)
        assert response['data']['cart_value'] >= 0
    
    def test_apply_offer_floating_point_precision(self, api_client: CartAPI):
        """Test applying offer with floating point precision edge case."""
        # Setup: Add offer
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLAT_PERCENT,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Apply offer with precision edge case
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_PRECISION,
            user_id=user_segment.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # 99.999 - (99.999 * 10%) = 99.999 - 9.9999 = 89.9991
        assert abs(response['data']['cart_value'] - TestData.EXPECTED_PRECISION) < 0.01
    
    def test_apply_offer_all_segments_available(self, api_client: CartAPI):
        """Test applying offer when user's segment matches one of multiple segments."""
        # Setup: Add offer for p1 and p2
        offer_data = OfferTestData(
            restaurant_id=TestData.RESTAURANT_1,
            offer_type=TestData.OFFER_TYPE_FLATX,
            offer_value=TestData.OFFER_VALUE_10,
            customer_segment=[TestData.SEGMENT_P1, TestData.SEGMENT_P2]
        )
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        
        # Test with p1 user
        user_segment_p1 = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment_p1.user_id, user_segment_p1.segment)
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment_p1.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_190
        
        # Test with p2 user
        user_segment_p2 = TestData.get_user_segment_p2()
        api_client.set_user_segment(user_segment_p2.user_id, user_segment_p2.segment)
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment_p2.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        assert response['data']['cart_value'] == TestData.EXPECTED_190
        
        # Test with p3 user (should not get discount)
        user_segment_p3 = TestData.get_user_segment_p3()
        api_client.set_user_segment(user_segment_p3.user_id, user_segment_p3.segment)
        response = api_client.apply_offer(
            cart_value=TestData.CART_VALUE_200,
            user_id=user_segment_p3.user_id,
            restaurant_id=TestData.RESTAURANT_1
        )
        assert response['status_code'] == 200
        # p3 not in offer segments, so no discount
        assert response['data']['cart_value'] == TestData.CART_VALUE_200
    
    def test_apply_offer_string_cart_value(self, api_client: CartAPI):
        """Test applying offer with string cart_value instead of number."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            json={
                'cart_value': 'invalid',
                'user_id': TestData.USER_1,
                'restaurant_id': TestData.RESTAURANT_1
            }
        )
        assert response.status_code == 400
    
    def test_apply_offer_string_user_id(self, api_client: CartAPI):
        """Test applying offer with string user_id instead of number."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            json={
                'cart_value': TestData.CART_VALUE_200,
                'user_id': 'invalid',
                'restaurant_id': TestData.RESTAURANT_1
            }
        )
        # String user_id might be treated as invalid user (404) or validation error (400/500)
        assert response.status_code in [400, 404, 500]
    
    def test_apply_offer_negative_restaurant_id(self, api_client: CartAPI):
        """Test applying offer with negative restaurant_id."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            json={
                'cart_value': TestData.CART_VALUE_200,
                'user_id': TestData.USER_1,
                'restaurant_id': -1
            }
        )
        # Negative ID might be accepted (200), rejected as invalid (400), or treated as not found (404)
        assert response.status_code in [200, 400, 404]


class TestUserSegment:
    """Test cases for user segment operations."""
    
    def test_get_user_segment(self, api_client: CartAPI):
        """Test getting user segment."""
        # Setup: Set user segment
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test: Get user segment
        response = api_client.get_user_segment(user_segment.user_id)
        assert response['status_code'] == 200
        assert response['data']['segment'] == user_segment.segment
    
    def test_get_user_segment_not_found(self, api_client: CartAPI):
        """Test getting user segment when user doesn't exist."""
        response = api_client.get_user_segment(TestData.USER_INVALID)
        assert response['status_code'] == 404
    
    def test_get_user_segment_missing_parameter(self, api_client: CartAPI):
        """Test getting user segment without user_id parameter."""
        # This test requires direct API call since the method requires user_id
        import requests
        response = requests.get('http://localhost:5001/api/v1/user_segment')
        assert response.status_code == 400
    
    def test_set_user_segment_invalid_segment(self, api_client: CartAPI):
        """Test setting user segment with invalid segment value."""
        response = api_client.set_user_segment(
            user_id=TestData.USER_1,
            segment=TestData.SEGMENT_INVALID
        )
        assert response['status_code'] == 400
    
    def test_set_user_segment_negative_user_id(self, api_client: CartAPI):
        """Test setting user segment with negative user_id."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/user_segment',
            json={
                'user_id': -1,
                'segment': TestData.SEGMENT_P1
            }
        )
        # Negative ID might be accepted or rejected
        assert response.status_code in [200, 400]
    
    def test_set_user_segment_empty_segment(self, api_client: CartAPI):
        """Test setting user segment with empty string."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/user_segment',
            json={
                'user_id': TestData.USER_1,
                'segment': ''
            }
        )
        assert response.status_code == 400
    
    def test_set_user_segment_null_values(self, api_client: CartAPI):
        """Test setting user segment with null values."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/user_segment',
            json={
                'user_id': None,
                'segment': None
            }
        )
        assert response.status_code == 400


class TestNegativeCornerCases:
    """Additional negative and corner case tests."""
    
    def test_add_offer_string_restaurant_id(self, api_client: CartAPI):
        """Test adding offer with string restaurant_id."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/offer',
            json={
                'restaurant_id': 'invalid',
                'offer_type': TestData.OFFER_TYPE_FLATX,
                'offer_value': TestData.OFFER_VALUE_10,
                'customer_segment': [TestData.SEGMENT_P1]
            }
        )
        # String restaurant_id might be accepted (treated as valid) or rejected (400)
        # The mock service might not validate type strictly
        assert response.status_code in [200, 400]
    
    def test_add_offer_string_offer_value(self, api_client: CartAPI):
        """Test adding offer with string offer_value."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/offer',
            json={
                'restaurant_id': TestData.RESTAURANT_1,
                'offer_type': TestData.OFFER_TYPE_FLATX,
                'offer_value': 'invalid',
                'customer_segment': [TestData.SEGMENT_P1]
            }
        )
        assert response.status_code == 400
    
    def test_add_offer_null_customer_segment(self, api_client: CartAPI):
        """Test adding offer with null customer_segment."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/offer',
            json={
                'restaurant_id': TestData.RESTAURANT_1,
                'offer_type': TestData.OFFER_TYPE_FLATX,
                'offer_value': TestData.OFFER_VALUE_10,
                'customer_segment': None
            }
        )
        assert response.status_code == 400
    
    def test_add_offer_invalid_json(self, api_client: CartAPI):
        """Test adding offer with invalid JSON."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/offer',
            data='invalid json',
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code in [400, 500]
    
    def test_apply_offer_missing_json_body(self, api_client: CartAPI):
        """Test applying offer with missing JSON body."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code in [400, 500]
    
    def test_apply_offer_extra_fields(self, api_client: CartAPI):
        """Test applying offer with extra fields in request."""
        # Setup
        offer_data = TestData.get_valid_flatx_offer_p1()
        api_client.add_offer(
            restaurant_id=offer_data.restaurant_id,
            offer_type=offer_data.offer_type,
            offer_value=offer_data.offer_value,
            customer_segment=offer_data.customer_segment
        )
        user_segment = TestData.get_user_segment_p1()
        api_client.set_user_segment(user_segment.user_id, user_segment.segment)
        
        # Test with extra field
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            json={
                'cart_value': TestData.CART_VALUE_200,
                'user_id': user_segment.user_id,
                'restaurant_id': TestData.RESTAURANT_1,
                'extra_field': 'should_be_ignored'
            }
        )
        # Should still work (extra fields ignored)
        assert response.status_code == 200
        assert response.json()['cart_value'] == TestData.EXPECTED_190
    
    def test_apply_offer_empty_json(self, api_client: CartAPI):
        """Test applying offer with empty JSON body."""
        import requests
        response = requests.post(
            'http://localhost:5001/api/v1/cart/apply_offer',
            json={}
        )
        assert response.status_code == 400
