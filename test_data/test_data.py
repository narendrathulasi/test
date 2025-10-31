"""
Test data constants and fixtures for cart offer tests.
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OfferTestData:
    """Test data for offer creation."""
    restaurant_id: int
    offer_type: str
    offer_value: float
    customer_segment: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            'restaurant_id': self.restaurant_id,
            'offer_type': self.offer_type,
            'offer_value': self.offer_value,
            'customer_segment': self.customer_segment
        }


@dataclass
class CartTestData:
    """Test data for cart operations."""
    cart_value: float
    user_id: int
    restaurant_id: int
    expected_cart_value: float = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            'cart_value': self.cart_value,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id
        }


@dataclass
class UserSegmentTestData:
    """Test data for user segment operations."""
    user_id: int
    segment: str


class TestData:
    """Centralized test data constants."""
    
    # Restaurant IDs
    RESTAURANT_1 = 1
    RESTAURANT_2 = 2
    RESTAURANT_3 = 3
    RESTAURANT_INVALID = 999
    
    # User IDs
    USER_1 = 1
    USER_2 = 2
    USER_3 = 3
    USER_INVALID = 999
    
    # Customer Segments
    SEGMENT_P1 = 'p1'
    SEGMENT_P2 = 'p2'
    SEGMENT_P3 = 'p3'
    SEGMENT_INVALID = 'p4'
    
    # Offer Types
    OFFER_TYPE_FLATX = 'FLATX'
    OFFER_TYPE_FLAT_PERCENT = 'FLAT%'
    OFFER_TYPE_INVALID = 'INVALID'
    
    # Offer Values
    OFFER_VALUE_10 = 10.0
    OFFER_VALUE_15 = 15.0
    OFFER_VALUE_20 = 20.0
    OFFER_VALUE_50 = 50.0
    OFFER_VALUE_100 = 100.0
    OFFER_VALUE_12_5 = 12.5
    OFFER_VALUE_NEGATIVE = -10.0
    OFFER_VALUE_ZERO = 0.0
    OFFER_VALUE_101 = 101.0  # > 100% for percentage
    OFFER_VALUE_0_01 = 0.01  # Very small value
    OFFER_VALUE_999999 = 999999.0  # Very large value
    
    # Cart Values
    CART_VALUE_200 = 200.0
    CART_VALUE_100 = 100.0
    CART_VALUE_100_50 = 100.50
    CART_VALUE_30 = 30.0
    CART_VALUE_10 = 10.0  # Exactly equals discount
    CART_VALUE_ZERO = 0.0
    CART_VALUE_0_01 = 0.01  # Very small value
    CART_VALUE_999999 = 999999.0  # Very large value
    CART_VALUE_PRECISION = 99.999  # Floating point precision test
    
    # Expected Results
    EXPECTED_190 = 190.0  # 200 - 10
    EXPECTED_180 = 180.0  # 200 - (200 * 10%)
    EXPECTED_170 = 170.0  # 200 - (200 * 15%)
    EXPECTED_0 = 0.0
    EXPECTED_87_94 = 87.94  # 100.50 - (100.50 * 12.5%)
    EXPECTED_PRECISION = 89.9991  # 99.999 - (99.999 * 10%)
    
    @classmethod
    def get_valid_flatx_offer_p1(cls) -> OfferTestData:
        """Get valid FLATX offer for p1 segment."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_FLATX,
            offer_value=cls.OFFER_VALUE_10,
            customer_segment=[cls.SEGMENT_P1]
        )
    
    @classmethod
    def get_valid_flat_percent_offer_p2(cls) -> OfferTestData:
        """Get valid FLAT% offer for p2 segment."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_FLAT_PERCENT,
            offer_value=cls.OFFER_VALUE_10,
            customer_segment=[cls.SEGMENT_P2]
        )
    
    @classmethod
    def get_valid_flat_percent_offer_multiple_segments(cls) -> OfferTestData:
        """Get valid FLAT% offer for multiple segments."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_FLAT_PERCENT,
            offer_value=cls.OFFER_VALUE_15,
            customer_segment=[cls.SEGMENT_P1, cls.SEGMENT_P2]
        )
    
    @classmethod
    def get_offer_invalid_type(cls) -> OfferTestData:
        """Get offer with invalid type."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_INVALID,
            offer_value=cls.OFFER_VALUE_10,
            customer_segment=[cls.SEGMENT_P1]
        )
    
    @classmethod
    def get_offer_invalid_segment(cls) -> OfferTestData:
        """Get offer with invalid segment."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_FLATX,
            offer_value=cls.OFFER_VALUE_10,
            customer_segment=[cls.SEGMENT_INVALID]
        )
    
    @classmethod
    def get_offer_negative_value(cls) -> OfferTestData:
        """Get offer with negative value."""
        return OfferTestData(
            restaurant_id=cls.RESTAURANT_1,
            offer_type=cls.OFFER_TYPE_FLATX,
            offer_value=cls.OFFER_VALUE_NEGATIVE,
            customer_segment=[cls.SEGMENT_P1]
        )
    
    @classmethod
    def get_cart_apply_offer_p1(cls) -> CartTestData:
        """Get cart data for applying offer to p1 user."""
        return CartTestData(
            cart_value=cls.CART_VALUE_200,
            user_id=cls.USER_1,
            restaurant_id=cls.RESTAURANT_1,
            expected_cart_value=cls.EXPECTED_190
        )
    
    @classmethod
    def get_cart_apply_offer_p2(cls) -> CartTestData:
        """Get cart data for applying offer to p2 user."""
        return CartTestData(
            cart_value=cls.CART_VALUE_200,
            user_id=cls.USER_2,
            restaurant_id=cls.RESTAURANT_1,
            expected_cart_value=cls.EXPECTED_180
        )
    
    @classmethod
    def get_user_segment_p1(cls) -> UserSegmentTestData:
        """Get user segment data for p1."""
        return UserSegmentTestData(
            user_id=cls.USER_1,
            segment=cls.SEGMENT_P1
        )
    
    @classmethod
    def get_user_segment_p2(cls) -> UserSegmentTestData:
        """Get user segment data for p2."""
        return UserSegmentTestData(
            user_id=cls.USER_2,
            segment=cls.SEGMENT_P2
        )
    
    @classmethod
    def get_user_segment_p3(cls) -> UserSegmentTestData:
        """Get user segment data for p3."""
        return UserSegmentTestData(
            user_id=cls.USER_3,
            segment=cls.SEGMENT_P3
        )

