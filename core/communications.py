import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class HarmonyVintageMailer:
    """
    Secure outbound email dispatcher for Harmony Vintage.
    Handles the final step of the autonomous supply chain loop.
    """
    def __init__(self):
        # We will use Gmail's secure SMTP server for the prototype
        self.email_address = os.getenv("HV_SENDER_EMAIL")
        self.email_password = os.getenv("HV_SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    def dispatch_supplier_email(self, target_email: str, subject: str, body: str) -> dict:
        """Assembles and securely transmits the AI-generated procurement request."""
        if not self.email_address or not self.email_password:
            print("[Harmony Vintage WARNING] Email credentials missing. Simulating dispatch...")
            return {"success": True, "message": "Simulated! (Add HV_SENDER_EMAIL to .env to send real emails)"}
        
        try:
            print(f"[Harmony Vintage] Connecting to secure SMTP server to email {target_email}...")
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = f"Harmony Vintage Procurement <{self.email_address}>"
            msg['To'] = target_email
            msg.set_content(body)

            # Establish a secure SSL connection to the mail server
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            
            print("[Harmony Vintage] Sourcing request successfully dispatched.")
            return {"success": True, "message": "Email dispatched to factory successfully."}
            
        except Exception as e:
            print(f"[Harmony Vintage Mailer ERROR] Transmission failed: {e}")
            return {"success": False, "message": str(e)}