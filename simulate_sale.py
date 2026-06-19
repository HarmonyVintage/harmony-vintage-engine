import requests
import json
import time

print("\n[Simulation] A customer just clicked 'Checkout' on the Harmony Vintage storefront...")
time.sleep(2)

# This mimics the exact JSON data packet Shopify sends when an order is placed
shopify_payload = {
    "order_id": "#HV-9042",
    "line_items": [
        {
            "sku": "HV-TEE-OVR-XL",
            "name": "Oversized Box Tee (Cream - XL)",
            "quantity": 2
        }
    ]
}

# Firing the data packet at your running local server
try:
    response = requests.post("http://127.0.0.1:5000/api/webhook/shopify", json=shopify_payload)
    print(f"[Simulation] Server responded with: {response.json()}")
except Exception as e:
    print(f"Failed to connect: {e}")