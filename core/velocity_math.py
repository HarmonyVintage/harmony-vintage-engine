import datetime

class HarmonyVintageVelocity:
    """
    Predictive analytics engine for Harmony Vintage.
    Calculates sales velocity and forecasting metrics.
    """
    
    @staticmethod
    def calculate_daily_velocity(sales_history: list, days: int = 30) -> float:
        """
        Computes the average units sold per day over a given window.
        sales_history format: list of dicts -> [{'date': '2026-06-15', 'quantity': 5}]
        """
        if not sales_history:
            return 0.0
            
        total_units = sum(item['quantity'] for item in sales_history)
        velocity = total_units / days
        return round(float(velocity), 2)

    @staticmethod
    def compute_days_until_stockout(current_stock: int, daily_velocity: float) -> int:
        """
        Calculates how many days of inventory remain before a total blackout.
        """
        if daily_velocity <= 0:
            return 999  # Infinite supply if there are no active sales
            
        days_remaining = current_stock / daily_velocity
        return int(days_remaining)

    @staticmethod
    def evaluate_restock_trigger(current_stock: int, safety_threshold: int, days_remaining: int, lead_time_days: int) -> bool:
        """
        Determines if the Harmony Vintage engine needs to issue an autonomous sourcing request.
        
        Triggers True if:
        1. Current stock drops below the hard safety baseline.
        2. The remaining stock timeline is less than or equal to supplier factory production + transit times.
        """
        # Critical baseline breach
        if current_stock <= safety_threshold:
            print("[Harmony Vintage ALERT] Stock fell below absolute safety threshold.")
            return True
            
        # Lead time breach (Will hit zero before the new shipment can physically arrive at the warehouse)
        if days_remaining <= lead_time_days:
            print(f"[Harmony Vintage ALERT] Lead time bottleneck detected. Stockout risk in {days_remaining} days.")
            return True
            
        return False