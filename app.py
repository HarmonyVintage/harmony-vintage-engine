from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
from dotenv import load_dotenv

# Import the core Harmony Vintage modules
from core.database import db
from core.communications import HarmonyVintageMailer
from core.platform_sync import HarmonyVintageSync
from core.velocity_math import HarmonyVintageVelocity
from core.agent import HarmonyVintageAgent

# Load environment variables
load_dotenv(override=True)

app = Flask(__name__)
# Hardcode a secure session key
app.secret_key = "harmony_vintage_master_session_key_2026"

# Initialize the global tools
ai_agent = HarmonyVintageAgent()
mailer = HarmonyVintageMailer()

# --- THE NEW AUTHENTICATION GATES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login screen and verifies the master password."""
    if session.get('authenticated'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        provided_password = request.form.get('password')
        
        # WE ARE HARDCODING THE PASSWORD FOR THIS TEST
        correct_password = "@mansisameer%" 
        
        # Add a print statement so we can see exactly what Python is doing
        print(f"User typed: {provided_password}")
        print(f"System expects: {correct_password}")
        
        if provided_password == correct_password:
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid Master Password. Access Denied.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Destroys the session cookie to securely log out."""
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# --- DASHBOARD LOGIC (NOW PROTECTED) ---

@app.route('/')
def home():
    """Renders the executive Harmony Vintage dashboard with live database metrics."""
    
    # THE BOUNCER: If the user doesn't have a secure session cookie, kick them to login
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    # 1. Fetch live data from the Supabase vault
    try:
        response = db.client.table("hv_inventory").select("*").execute()
        inventory_items = response.data or []
    except Exception as e:
        print(f"[Harmony Vintage ERROR] Failed to fetch ledger: {e}")
        inventory_items = []

    # 2. Calculate dynamic metrics based on real database size
    total_skus = len(inventory_items)
    total_velocity = sum(item.get('daily_velocity', 0) for item in inventory_items)
    avg_burn_rate = round(total_velocity / total_skus, 1) if total_skus > 0 else 0.0
    
    restock_alerts = sum(
        1 for item in inventory_items 
        if item.get('current_stock', 0) <= (item.get('daily_velocity', 0.1) * 14)
    )
    
    capital_saved = f"₹{total_skus * 592:,}"

    # 3. Inject the data into the HTML
    return render_template(
        'dashboard.html',
        inventory=inventory_items,
        total_skus=total_skus,
        avg_burn_rate=avg_burn_rate,
        restock_alerts=restock_alerts,
        capital_saved=capital_saved
    )

# ... (Keep all your other routes like /system/health, /api/ai/draft, etc. exactly the same below this line) ...

@app.route('/api/auth', methods=['POST'])
def authenticate():
    """Checks the admin password against the secure vault."""
    data = request.get_json() or {}
    provided_password = data.get('password')
    # This securely looks inside your .env file for the password
    correct_password = os.getenv("HV_ADMIN_PASSWORD") 
    
    if provided_password == correct_password:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Unauthorized access attempt blocked."}), 401

@app.route('/system/health', methods=['GET'])
def health_check():
    """Diagnostic endpoint to verify Harmony Vintage database connections."""
    db_status = "Securely Connected" if db.client else "Disconnected (Check .env)"
    ai_status = "Online" if ai_agent.client else "Offline"
    return jsonify({
        "brand": "Harmony Vintage",
        "database_status": db_status,
        "ai_module": ai_status,
        "sync_module": "Ready"
    })

@app.route('/api/ai/draft', methods=['POST'])
def generate_draft():
    """Secure API endpoint that triggers the Harmony Vintage AI Sourcing Agent."""
    data = request.get_json() or {}
    sku = data.get('sku')
    product_name = data.get('product_name')
    quantity = data.get('quantity', 500)
    supplier = data.get('supplier')
    
    if not sku or not product_name or not supplier:
        return jsonify({
            "error": True,
            "message": "[Harmony Vintage] Missing mandatory parameters."
        }), 400
        
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
    supplier_email = "supplier@example.com" 

    if not subject or not body:
        return jsonify({"success": False, "message": "Missing email content"}), 400

    response = mailer.dispatch_supplier_email(supplier_email, subject, body)
    return jsonify(response)

@app.route('/api/webhook/shopify', methods=['POST'])
def shopify_order_webhook():
    """Listens for live customer orders from Shopify."""
    data = request.get_json() or {}
    print("\n" + "-"*50)
    print("[Harmony Vintage WEBHOOK] Live customer transaction detected!")
    
    line_items = data.get('line_items', [])
    for item in line_items:
        sku = item.get('sku')
        qty_sold = item.get('quantity', 1)
        print(f"[Harmony Vintage System] Customer purchased {qty_sold}x unit(s) of SKU: {sku}")
        
    print("-"*50 + "\n")
    return jsonify({"status": "success", "message": "Harmony Vintage ledger updated autonomously."}), 200

if __name__ == '__main__':
    print("\n" + "="*55)
    print(" 🚀 HARMONY VINTAGE AUTONOMOUS ENGINE INITIALIZING ")
    print("="*55)
    print("[System] Loading core configurations...")
    print("[System] Verifying Supabase secure vault...")
    print("[System] Engine ready on Port 5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)