import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class HarmonyVintageAgent:
    """
    Autonomous Communication Agent for Harmony Vintage.
    Generates structured supplier communication workflows based on inventory trends.
    """
    def __init__(self):
        # Initialize the next-gen Gemini client using the google-genai SDK
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[Harmony Vintage WARNING] GEMINI_API_KEY missing from environment variables.")
        
        # Safe initialization
        self.client = genai.Client(api_key=api_key) if api_key else None
        # Deploying the high-speed production model
        self.model_name = "gemini-2.5-flash"

    def draft_supplier_restock_email(self, sku: str, product_name: str, suggested_order_qty: int, supplier_name: str) -> dict:
        """
        Generates a highly optimized, structured restock request email.
        Forces the AI model to respond strictly in a parsed JSON schema.
        """
        if not self.client:
            return {
                "error": True,
                "message": "AI Engine offline. Verify GEMINI_API_KEY."
            }

        # Establish strict operational boundaries for the AI context
        system_instruction = (
            "You are the elite automated procurement manager for 'Harmony Vintage', a premium custom apparel brand. "
            "Your objective is to generate clear, professional, and firm B2B restock emails to international clothing manufacturers. "
            "Maintain an authoritative yet collaborative corporate tone. Do not include casual filler text or pleasantries."
        )

        prompt = (
            f"Draft a production restock order request for supplier '{supplier_name}'.\n"
            f"Product Details:\n"
            f"- SKU: {sku}\n"
            f"- Description: {product_name}\n"
            f"- Proposed Order Quantity: {suggested_order_qty} units\n\n"
            f"You must output a single JSON object containing exactly three keys: 'email_subject', 'email_body', and 'factory_action_required'."
        )

        try:
            print(f"[Harmony Vintage AI] Analyzing supply chain data for SKU: {sku}...")
            
            # Requesting structured schema generation to eliminate parsing errors
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "email_subject": types.Schema(type=types.Type.STRING),
                            "email_body": types.Schema(type=types.Type.STRING),
                            "factory_action_required": types.Schema(type=types.Type.STRING)
                        },
                        required=["email_subject", "email_body", "factory_action_required"]
                    ),
                    temperature=0.2  # Kept low to enforce predictability and eliminate creative variance
                )
            )

            # Safeguard parsing into native Python dict structures
            generated_data = json.loads(response.text)
            print("[Harmony Vintage AI] Production draft generated successfully.")
            return generated_data

        except Exception as e:
            print(f"[Harmony Vintage AI ERROR] Generative validation failed: {e}")
            return {
                "error": True,
                "message": f"Failed to compile prompt stream: {str(e)}"
            }