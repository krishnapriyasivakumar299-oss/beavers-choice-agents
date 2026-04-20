# beaver_agents.py

from project_starter import (
    create_transaction,
    get_stock_level,
    get_supplier_delivery_date
)


class InventoryAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, item_id: int):

        df = get_stock_level(item_id, "2024-12-31")

        if df is None or df.empty:
            stock = 0
        else:
            stock = int(df["current_stock"].iloc[0])

        if stock < 10:
            return {
                "status": "low",
                "stock": stock,
                "eta": get_supplier_delivery_date("2024-12-31", 10)
            }

        return {"status": "ok", "stock": stock}


class QuoteAgent:
    def run(self, customer_id: int, item_id: int, quantity: int):
        base_price = 10

        if quantity >= 100:
            total = base_price * quantity * 0.9
            reason = "Bulk discount"
        else:
            total = base_price * quantity
            reason = "Standard pricing"

        return {"quote": total, "reason": reason}


class SalesAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, order: dict):
        return create_transaction(
            self.engine,
            "sale",
            order["item_id"],
            order["quantity"],
            order["price"]
        )

class FinanceAgent:
    def run(self):
        return {"message": "Finance summary placeholder"}

class OrchestratorAgent:
    def __init__(self, engine):
        self.inventory = InventoryAgent(engine)
        self.quote = QuoteAgent()
        self.sales = SalesAgent(engine)
        self.finance = FinanceAgent()   # ✅ ADD

    def handle_request(self, request: dict):

        if request["type"] == "inventory":
            return self.inventory.run(request["item_id"])

        elif request["type"] == "quote":
            return self.quote.run(
                request["customer_id"],
                request["item_id"],
                request["quantity"]
            )

        elif request["type"] == "sale":
            return self.sales.run(request["order"])

        elif request["type"] == "finance":
            return self.finance.run()   # ✅ ADD

        else:
            return {"error": "Unknown request"}