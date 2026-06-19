import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HarmonyVintageSync:
    """
    Core synchronization engine for Harmony Vintage.
    Handles secure GraphQL connections to Shopify storefronts.
    """
    def __init__(self, shop_url: str, access_token: str):
        self.shop_url = shop_url
        self.access_token = access_token
        # Using the latest 2026-04 API version for compliance
        self.graphql_endpoint = f"https://{self.shop_url}/admin/api/2026-04/graphql.json"
        
        # System identification for the API calls
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
            "User-Agent": "Harmony Vintage Autonomous Engine v1.0"
        }

    def fetch_inventory_levels(self):
        """
        Pulls real-time stock levels for the Harmony Vintage ecosystem.
        """
        # GraphQL query requesting exact SKUs and inventory counts
        query = """
        {
          products(first: 50) {
            edges {
              node {
                title
                variants(first: 10) {
                  edges {
                    node {
                      sku
                      inventoryQuantity
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            print("[Harmony Vintage] Initiating secure inventory sync...")
            response = requests.post(
                self.graphql_endpoint, 
                json={"query": query}, 
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            print("[Harmony Vintage] Sync successful. Processing SKUs.")
            return self._parse_graphql_inventory(data)
            
        except requests.exceptions.RequestException as e:
            print(f"[Harmony Vintage ERROR] Sync failed: {e}")
            return None

    def _parse_graphql_inventory(self, raw_data):
        """Formats the raw GraphQL response for the Harmony Vintage database."""
        inventory_list = []
        try:
            products = raw_data['data']['products']['edges']
            for product in products:
                product_name = product['node']['title']
                variants = product['node']['variants']['edges']
                
                for variant in variants:
                    sku = variant['node']['sku']
                    stock = variant['node']['inventoryQuantity']
                    
                    if sku:  # Only track items with active SKUs
                        inventory_list.append({
                            "product_name": product_name,
                            "sku": sku,
                            "current_stock": stock
                        })
            return inventory_list
        except KeyError as e:
            print(f"[Harmony Vintage ERROR] Data parsing failed: {e}")
            return []