"""
Multi-tenant Corporate Subscription Engine 


Let's move on to account management. At Ramp, companies buy premium SaaS subscription tiers to manage their team expenses. 
Each company has a fixed billing cycle duration.

Your task is to design a Subscription Billing Lifecycle Manager. 
The engine must allow companies to register for a subscription tier, handle manual renewals, 
upgrade their tier mid-cycle via partial pro-rated credit math, and identify which companies have expired subscriptions 
as of a specific logical timestamp.


""" 

class SubscriptionManagementEngine:

    def __init__(self):

        # pricing tier map
        self.pricing_tier = {
            "BASIC": 100.0,
            "PREMIUM": 300.0,
            "ENTERPRISE": 1000.0
        }

        # 2. Standard cycle duration definition (e.g, 30 arbitrary time units)
        self.CYCLE_DURATION = 30

        # 3. Main database storage layout:
        # Maps {company_id -> {"tier": str, "cycle_start": int, "cycle_end": int, "credits": float}}
        self.subscriptions = {}
    
    def subscribe(self, company_id: str, tier: str, start_time: int) -> None:
        """
        Registers brand new company for initial cycle block 

        """

        # normalize input strings
        tier = tier.upper()
        company_id = company_id.lower()

        if tier not in self.pricing_tier:
            raise ValueError(f"Invalid tier target {tier}")
        

        # compute end_time
        end_time = start_time + self.CYCLE_DURATION

        # Initialize the state entry mapping a fresh company with 0 starting credits.
        self.subscriptions[company_id] = {
            "tier": tier,
            "cycle_start": start_time,
            "cycle_end": end_time,
            "credits": 0.0
        }
        print(f" [SUBSCRIBE] Company '{company_id}' onboarded to {tier}. Active until T={end_time}")
    
    def upgrade_tier(self, company_id: str, new_tier: str, current_time: int) -> dict:
        """

        Upgrades a company's tier mid-cycle.
        Computes unspent pro-rated values as credits and applies them dynamically to the new tier 
        configuration cost.

        """

        # Normalize the strings 
        new_tier = new_tier.upper()
        company_id = company_id.lower()

        if new_tier not in self.pricing_tier:
            raise ValueError(f"Invalid tier target {new_tier}")

        current_sub = self.subscriptions.get(company_id)
        if not current_sub:
            raise KeyError(f"Company '{company_id}' does not possess an active registration profile.")
        
        # Guard Check: Ensure company is downgrading their subcription 
        if self.pricing_tier[new_tier] <= self.pricing_tier[current_sub["tier"]]:
            return {"status": "REJECTED", "reason": "Upgrade target must cost more than current active tier."}
        
        # Compute Pro-Rated Credit Unused Value 
        total_duration = current_sub["cycle_end"] - current_sub["cycle_start"]
        remaining_time = current_sub["cycle_end"] - current_time

        # if past active time period to upgrade, reject:
        if remaining_time <= 0:
            return {"status": "REJECTED", "reason": "Active cycle has expired. Perform a clean renewal instead."}

        
        # Calculate exact fraction of unspent time remaining in the current cycle
        unspent_fraction = remaining_time / total_duration
        current_tier_cost = self.pricing_tier[current_sub["tier"]]

        # pro-rated cash return compute
        refund = unspent_fraction * current_tier_cost

        # Compute cost of new tier for additional days 
        new_tier_cost = self.pricing_tier[new_tier]
        pro_rated_new_cost = new_tier_cost * unspent_fraction

        net_charge_due = pro_rated_new_cost - refund

        # Update account ledger in place 
        current_sub["tier"] = new_tier

        # Return summary report data to the caller for execution tracking 
        return {
            "status": "UPGRADED",
            "company_id": company_id,
            "refund_credit_applied": round(refund, 2),
            "net_amount_charged": round(net_charge_due, 2)
        }
    
    def get_expired_companies(self, check_time: int) -> list:
        """
        Scans the active db mappings and aggregates a list of all 
        company IDs whose billing cycle end timestamp is strictly less than or equal to the 
        check_time. 

        """

        expired_list = []

        # use clean key-value dictionary iteration to parse our records stream
        for company_id, details in self.subscriptions.items():
            if details["cycle_end"] <= check_time:
                expired_list.append(company_id)
        
        return expired_list


if __name__ == "__main__":
    engine = SubscriptionManagementEngine()
    print("--------- Testing Subscription Lifecycle Engine ---------")

    # Day 0: Alpha Corp signs up for BASIC tier ($100/cycle)
    engine.subscribe("alpha_corp", "BASIC", start_time=0)


    # DAY 15: Alpha Corp decides to upgrade to PREMIUM ($300/cycle) mid-way through their cycle.
    # Calculation Check:
    # Remaining time = 15 days out of 30 (0.5 remaining fraction).
    # Unused Basic Credit = $100 * 0.5 = $50.00
    # Pro-rated Premium cost for 15 days = $300 * 0.5 = $150.00
    # Net Balance Due = $150.00 - $50 = $100.00
    upgrade_receipt = engine.upgrade_tier("alpha_corp", "PREMIUM", current_time=15)
    print(f"Upgrade Result: {upgrade_receipt}")

    assert upgrade_receipt["refund_credit_applied"] == 50.00
    assert upgrade_receipt["net_amount_charged"] == 100.00

    print(" ✅ Pro-rated upgrade credit matching offsets verified successfully.")

    assert "alpha_corp" not in engine.get_expired_companies(29)
    assert "alpha_corp" in engine.get_expired_companies(30)
    print(" ✅ Expiration timeline boundary sweeps validated perfectly.")

    print("\n🚀 [SYSTEM SUCCESS] Problem 2 cleared! Let me know when you're ready for Problem 3.")