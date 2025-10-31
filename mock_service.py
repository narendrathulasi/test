"""
Mock service for Zomato cart offer testing.
This service simulates the API endpoints for offers and cart operations.
"""
from flask import Flask, request, jsonify
from typing import Dict, List, Optional

app = Flask(__name__)

# In-memory storage for offers
# Structure: {restaurant_id: {segment: {offer_type, offer_value}}}
offers_db: Dict[int, Dict[str, Dict[str, any]]] = {}

# In-memory storage for user segments
# Structure: {user_id: segment}
user_segments_db: Dict[int, str] = {}


@app.route('/api/v1/offer', methods=['POST'])
def add_offer():
    """
    Add offer to a restaurant for customer segments.
    
    Request body:
    {
        "restaurant_id": 1,
        "offer_type": "FLATX",  # or "FLAT%"
        "offer_value": 10,
        "customer_segment": ["p1"]
    }
    """
    try:
        data = request.json
        
        restaurant_id = data.get('restaurant_id')
        offer_type = data.get('offer_type')
        offer_value = data.get('offer_value')
        customer_segments = data.get('customer_segment', [])
        
        # Validate required fields
        if not all([restaurant_id, offer_type, offer_value, customer_segments]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Validate offer_type
        if offer_type not in ['FLATX', 'FLAT%']:
            return jsonify({"error": "Invalid offer_type. Must be 'FLATX' or 'FLAT%'"}), 400
        
        # Validate offer_value
        try:
            offer_value = float(offer_value)
            if offer_value < 0:
                return jsonify({"error": "offer_value must be non-negative"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "offer_value must be a number"}), 400
        
        # Validate customer segments
        valid_segments = ['p1', 'p2', 'p3']
        for segment in customer_segments:
            if segment not in valid_segments:
                return jsonify({"error": f"Invalid segment: {segment}. Must be one of {valid_segments}"}), 400
        
        # Initialize restaurant offers if not exists
        if restaurant_id not in offers_db:
            offers_db[restaurant_id] = {}
        
        # Add offers for each segment
        for segment in customer_segments:
            offers_db[restaurant_id][segment] = {
                'offer_type': offer_type,
                'offer_value': offer_value
            }
        
        return jsonify({"response_msg": "success"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/cart/apply_offer', methods=['POST'])
def apply_offer():
    """
    Apply offer to cart based on user segment and restaurant.
    
    Request body:
    {
        "cart_value": 200,
        "user_id": 1,
        "restaurant_id": 1
    }
    """
    try:
        data = request.json
        
        cart_value = data.get('cart_value')
        user_id = data.get('user_id')
        restaurant_id = data.get('restaurant_id')
        
        # Validate required fields
        if not all([cart_value, user_id, restaurant_id]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Validate cart_value
        try:
            cart_value = float(cart_value)
            if cart_value < 0:
                return jsonify({"error": "cart_value must be non-negative"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "cart_value must be a number"}), 400
        
        # Get user segment
        segment = user_segments_db.get(user_id)
        if not segment:
            return jsonify({"error": "User segment not found"}), 404
        
        # Check if restaurant has offers
        if restaurant_id not in offers_db:
            # No offer available, return original cart value
            return jsonify({"cart_value": cart_value}), 200
        
        # Check if segment has offer for this restaurant
        restaurant_offers = offers_db[restaurant_id]
        if segment not in restaurant_offers:
            # No offer for this segment, return original cart value
            return jsonify({"cart_value": cart_value}), 200
        
        # Get offer details
        offer = restaurant_offers[segment]
        offer_type = offer['offer_type']
        offer_value = offer['offer_value']
        
        # Calculate discounted cart value
        if offer_type == 'FLATX':
            # Flat amount off
            final_cart_value = max(0, cart_value - offer_value)
        elif offer_type == 'FLAT%':
            # Flat percentage off
            discount_amount = (cart_value * offer_value) / 100
            final_cart_value = max(0, cart_value - discount_amount)
        else:
            return jsonify({"error": "Invalid offer type"}), 500
        
        # Round to 2 decimal places
        final_cart_value = round(final_cart_value, 2)
        
        return jsonify({"cart_value": final_cart_value}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/user_segment', methods=['GET'])
def get_user_segment():
    """
    Get user segment.
    
    Query params:
    - user_id: integer
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing user_id parameter"}), 400
        
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "user_id must be an integer"}), 400
        
        segment = user_segments_db.get(user_id)
        if not segment:
            return jsonify({"error": "User segment not found"}), 404
        
        return jsonify({"segment": segment}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/user_segment', methods=['POST'])
def set_user_segment():
    """
    Set user segment (helper endpoint for testing).
    
    Request body:
    {
        "user_id": 1,
        "segment": "p1"
    }
    """
    try:
        data = request.json
        
        user_id = data.get('user_id')
        segment = data.get('segment')
        
        if not all([user_id, segment]):
            return jsonify({"error": "Missing required fields"}), 400
        
        valid_segments = ['p1', 'p2', 'p3']
        if segment not in valid_segments:
            return jsonify({"error": f"Invalid segment. Must be one of {valid_segments}"}), 400
        
        user_segments_db[user_id] = segment
        
        return jsonify({"response_msg": "success"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

