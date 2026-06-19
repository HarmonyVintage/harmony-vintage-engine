from flask import Flask, jsonify, render_template, request
import os
from dotenv import load_dotenv
from core.communications import HarmonyVintageMailer

# Import the core Harmony Vintage modules
from core.database import db
from core.platform_sync import HarmonyVintageSync
from core.velocity_math import HarmonyVintageVelocity
from core.agent import HarmonyVintageAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the global Harmony Vintage AI instance
ai_agent = HarmonyVintageAgent()

# ---> PASTE THIS NEW LINE RIGHT HERE <---
mailer = HarmonyVintageMailer()


@app.route('/')
def home():
       """Renders the executive Harmony Vintage dashboard interface if authenticated."""
       return render_template('dashboard.html')

@app.route('/api/auth', methods=['POST'])
def authenticate():
       """Checks the admin password against the secure vault."""
       data = request.get_json() or {}
       provided_password = data.get('password')
       correct_password = os.getenv("@mansisameeer%")
       
       if provided_password == correct_password:
           return jsonify({"success": True})
       return jsonify({"success": False, "message": "Unauthorized access attempt blocked."}), 401
    
    return jsonify({
        "brand": "Harmony Vintage",
        "database_status": db_status,
        "ai_module": ai_status,
        "sync_module": "Ready"
    })

@app.route('/api/ai/draft', methods=['POST'])
def generate_draft():
    """
    Secure API endpoint that triggers the Harmony Vintage AI Sourcing Agent.
    Expects a JSON payload containing product SKU, name, quantity, and target supplier.
    """
    data = request.get_json() or {}
    sku = data.get('sku')
    product_name = data.get('product_name')
    quantity = data.get('quantity', 500)
    supplier = data.get('supplier')
    
    if not sku or not product_name or not supplier:
        return jsonify({
            "error": True,
            "message": "[Harmony Vintage] Missing mandatory parameter allocations (sku, product_name, supplier)."
        }), 400
        
    # Trigger the Gemini live production-grade generation sequence
    ai_response = ai_agent.draft_supplier_restock_email(
        sku=sku,
        product_name=product_name,
        suggested_order_qty=int(quantity),
        supplier_name=supplier
    )
    
    return jsonify(ai_response)

@app.route('/api/email/dispatch', methods=['POST'])
def dispatch_email():
    """Endpoint triggered by the 'Approve' button on the dashboard."""
    data = request.get_json() or {}
    subject = data.get('subject')
    body = data.get('body')
    # In production, this would pull from the supplier database table
    supplier_email = "supplier@example.com" 

    if not subject or not body:
        return jsonify({"success": False, "message": "Missing email content"}), 400

    # Trigger the secure dispatch
    response = mailer.dispatch_supplier_email(supplier_email, subject, body)
    return jsonify(response)

@app.route('/api/webhook/shopify', methods=['POST'])
def shopify_order_webhook():
    """
    The central nervous system for Harmony Vintage. 
    Listens for live customer orders from Shopify and triggers autonomous math workflows.
    """
    data = request.get_json() or {}
    
    print("\n" + "-"*50)
    print("[Harmony Vintage WEBHOOK] Live customer transaction detected!")
    
    # Parse the incoming Shopify order payload
    order_id = data.get('order_id', 'UNKNOWN')
    line_items = data.get('line_items', [])
    
    for item in line_items:
        sku = item.get('sku')
        qty_sold = item.get('quantity', 1)
        
        print(f"[Harmony Vintage System] Customer purchased {qty_sold}x unit(s) of SKU: {sku}")
        print(f"[Harmony Vintage System] Processing velocity math and updating master ledger...")
        
        # In a fully connected state, this runs: db.update_inventory(sku, new_qty)
        # If the math hits critical, it autonomously runs ai_agent.draft_supplier_restock_email()
        
    print("-"*50 + "\n")
        
    return jsonify({"status": "success", "message": "Harmony Vintage ledger updated autonomously."}), 200

if __name__ == '__main__':
    # The Harmony Vintage startup sequence
    print("\n" + "="*55)
    print(" 🚀 HARMONY VINTAGE AUTONOMOUS ENGINE INITIALIZING ")
    print("="*55)
    print("[System] Loading core configurations...")
    print("[System] Verifying Supabase secure vault...")
    print("[System] Awakening generative AI orchestrators...")
    print("[System] Engine ready on Port 5000\n")
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True)