"""
API client classes for Zomato cart offer operations.
"""
import requests
from typing import Dict, List, Optional, Any


class CartAPI:
    """API client for cart and offer operations."""
    
    def __init__(self, base_url: str = 'http://localhost:5001'):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API server
        """
        self.base_url = base_url.rstrip('/')
    
    def add_offer(
        self,
        restaurant_id: int,
        offer_type: str,
        offer_value: float,
        customer_segment: List[str]
    ) -> Dict[str, Any]:
        """
        Add offer to a restaurant for customer segments.
        
        Args:
            restaurant_id: Restaurant ID
            offer_type: Type of offer ('FLATX' or 'FLAT%')
            offer_value: Offer value (amount or percentage)
            customer_segment: List of customer segments ['p1', 'p2', 'p3']
        
        Returns:
            Response dictionary
        """
        url = f'{self.base_url}/api/v1/offer'
        payload = {
            'restaurant_id': restaurant_id,
            'offer_type': offer_type,
            'offer_value': offer_value,
            'customer_segment': customer_segment
        }
        response = requests.post(url, json=payload)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else {}
        }
    
    def apply_offer(
        self,
        cart_value: float,
        user_id: int,
        restaurant_id: int
    ) -> Dict[str, Any]:
        """
        Apply offer to cart based on user segment and restaurant.
        
        Args:
            cart_value: Original cart value
            user_id: User ID
            restaurant_id: Restaurant ID
        
        Returns:
            Response dictionary with cart_value after discount
        """
        url = f'{self.base_url}/api/v1/cart/apply_offer'
        payload = {
            'cart_value': cart_value,
            'user_id': user_id,
            'restaurant_id': restaurant_id
        }
        response = requests.post(url, json=payload)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else {}
        }
    
    def get_user_segment(self, user_id: int) -> Dict[str, Any]:
        """
        Get user segment.
        
        Args:
            user_id: User ID
        
        Returns:
            Response dictionary with segment information
        """
        url = f'{self.base_url}/api/v1/user_segment'
        params = {'user_id': user_id}
        response = requests.get(url, params=params)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else {}
        }
    
    def set_user_segment(self, user_id: int, segment: str) -> Dict[str, Any]:
        """
        Set user segment (helper method for testing).
        
        Args:
            user_id: User ID
            segment: Customer segment ('p1', 'p2', or 'p3')
        
        Returns:
            Response dictionary
        """
        url = f'{self.base_url}/api/v1/user_segment'
        payload = {
            'user_id': user_id,
            'segment': segment
        }
        response = requests.post(url, json=payload)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else {}
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API server is healthy.
        
        Returns:
            Response dictionary
        """
        url = f'{self.base_url}/health'
        response = requests.get(url)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else {}
        }

