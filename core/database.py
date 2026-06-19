import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables securely
load_dotenv()

class HarmonyVintageDB:
    """
    Central database manager for the Harmony Vintage ecosystem.
    Handles all secure data routing to Supabase.
    """
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("[Harmony Vintage FATAL] Supabase credentials missing from .env")
            self.client = None
        else:
            self.client: Client = create_client(url, key)
            print("[Harmony Vintage] Secure Supabase connection established.")

    def update_inventory(self, store_id: str, sku: str, stock_level: int):
        """Routes real-time stock updates from the sync engine into the ledger."""
        if not self.client:
            return None
            
        try:
            response = (
                self.client.table("hv_inventory")
                .update({"current_stock": stock_level, "updated_at": "now()"})
                .eq("store_id", store_id)
                .eq("sku", sku)
                .execute()
            )
            return response
        except Exception as e:
            print(f"[Harmony Vintage DB ERROR] Failed to update SKU {sku}: {e}")
            return None

# Global instance for the Harmony Vintage application
db = HarmonyVintageDB()