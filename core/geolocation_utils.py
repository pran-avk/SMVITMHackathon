"""
Geolocation and QR Code Utilities for ArtScope
"""
import qrcode
from io import BytesIO
from django.core.files import File
from geopy.distance import geodesic
import json


def generate_qr_code(artwork):
    """
    Generate QR code for artwork
    Returns a File object that can be saved to the model
    """
    # Create QR code data with artwork info
    qr_data = {
        'artwork_id': str(artwork.id),
        'title': artwork.title,
        'museum': artwork.museum.name,
        'url': f'/api/artworks/{artwork.id}/'
    }
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return as Django File
    filename = f'qr_{artwork.id}.png'
    return File(buffer, name=filename)


def check_geofence(user_lat, user_lon, artwork_lat, artwork_lon, radius_meters):
    """
    Check if user is within the geofence radius of an artwork
    
    Args:
        user_lat: User's latitude
        user_lon: User's longitude
        artwork_lat: Artwork's latitude
        artwork_lon: Artwork's longitude
        radius_meters: Geofence radius in meters
    
    Returns:
        dict with 'allowed' (bool) and 'distance' (float in meters)
    """
    if not all([user_lat, user_lon, artwork_lat, artwork_lon]):
        return {
            'allowed': False,
            'distance': None,
            'message': 'Missing location data'
        }
    
    # Calculate distance
    user_coords = (float(user_lat), float(user_lon))
    artwork_coords = (float(artwork_lat), float(artwork_lon))
    distance = geodesic(user_coords, artwork_coords).meters
    
    # Check if within radius
    allowed = distance <= radius_meters
    
    return {
        'allowed': allowed,
        'distance': round(distance, 2),
        'message': f'You are {round(distance, 2)}m from this artwork' if not allowed else 'Access granted'
    }


def get_distance_message(distance_meters):
    """
    Get a user-friendly distance message
    """
    if distance_meters < 50:
        return "You're very close! Look around."
    elif distance_meters < 100:
        return "You're nearby. Walk a bit closer."
    elif distance_meters < 500:
        return f"You're {int(distance_meters)}m away from the museum."
    elif distance_meters < 1000:
        return f"You're {int(distance_meters)}m away. Head to the museum."
    else:
        km = distance_meters / 1000
        return f"You're {km:.1f}km away from the museum."
