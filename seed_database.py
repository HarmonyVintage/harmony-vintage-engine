import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Connect to Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# The starting inventory dataset
seed_data = [
    {"sku": "HV-POLO-BLK-M", "product_name": "Premium Pique Polo (Black - M)", "current_stock": 82, "daily_velocity": 14.2, "last_updated": "2026-06-19T10:00:00Z"},
    {"sku": "HV-HD-WHT-L", "product_name": "Vintage Heavyweight Hoodie (White - L)", "current_stock": 410, "daily_velocity": 8.1, "last_updated": "2026-06-19T10:00:00Z"},
    {"sku": "HV-TEE-OVR-XL", "product_name": "Oversized Box Tee (Cream - XL)", "current_stock": 12, "daily_velocity": 22.5, "last_updated": "2026-06-19T10:00:00Z"}
]

print("[System] Injecting starting data into Supabase vault...")
try:
    supabase.table("hv_inventory").insert(seed_data).execute()
    print("[Success] Data injected! Refresh your local dashboard.")
except Exception as e:
    print(f"[Error] Failed to inject data: {e}")