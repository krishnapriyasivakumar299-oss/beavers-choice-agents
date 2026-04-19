# beaver_agents.py
import ast
from smolagents import tool
from project_starter import (
    create_transaction,
    get_all_inventory,
    get_stock_level,
    get_supplier_delivery_date
)

# ------------------ TOOLS ------------------

@tool
def tool_create_transaction(order: dict) -> dict:
    """
    Finalize a sales transaction and update the database.

    Args:
        order (dict): A dictionary containing order details such as
                      customer_id, item_id, quantity, and price.

    Returns:
        dict: Confirmation of transaction and updated database state.
    """
    return create_transaction(order)

@tool
def tool_get_all_inventory() -> list:
    """Return the full inventory list."""
    return get_all_inventory()

@tool
def tool_get_stock_level(item_id: int, as_of_date: str = "today") -> int:
    """
    Check stock level for a specific item.

    Args:
        item_id (int): The unique identifier of the item to check.
        as_of_date (str): The date to check stock levels for (default: "today").

    Returns:
        int: Quantity of the item in stock.
    """
    df = get_stock_level(item_id, as_of_date)
    if df is None or df.empty:
        return 0
    value = df["current_stock"].iloc[0]
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@tool
def tool_get_supplier_delivery_date(item_id: int) -> str:
    """
    Estimate supplier delivery timeline for an item.

    Args:
        item_id (int): The unique identifier of the item.

    Returns:
        str: Expected delivery date from supplier.
    """
    return get_supplier_delivery_date(item_id)

# ---- Stubbed Finance Tools ----

@tool
def tool_get_cash_balance(as_of_date: str = "today") -> float:
    """
    Retrieve the current cash balance (stubbed).

    Args:
        as_of_date (str): The date to check cash balance for (default: "today").

    Returns:
        float: Fixed demo cash balance.
    """
    return 10000.0

@tool
def tool_generate_financial_report(as_of_date: str = "today") -> dict:
    """
    Generate a financial summary report (stubbed).

    Args:
        as_of_date (str): The date to generate the report for (default: "today").

    Returns:
        dict: Stubbed financial report.
    """
    return {"cash_change": 0, "summary": "Demo financial report"}

@tool
def tool_search_quote_history(customer_id: int) -> list:
    """
    Retrieve past quotes for a customer (stubbed).

    Args:
        customer_id (int): The unique identifier of the customer.

    Returns:
        list: List of past quotes for the customer.
    """
    return [
        {"customer_id": customer_id, "quote": 100, "reason": "Standard pricing"},
        {"customer_id": customer_id, "quote": 900, "reason": "Bulk discount applied"}
    ]

# ------------------ AGENTS ------------------

class InventoryAgent:
    def run(self, item_id: int) -> dict:
        stock = tool_get_stock_level(item_id)
        if stock < 10:
            return {"status": "low", "delivery": tool_get_supplier_delivery_date(item_id)}
        return {"status": "ok", "stock": stock}

class QuoteAgent:
    def run(self, customer_id: int, item_id: int, quantity: int) -> dict:
        history = tool_search_quote_history(customer_id)
        base_price = 10
        if quantity >= 100:
            price = base_price * quantity * 0.9
            reason = "Bulk discount applied"
        else:
            price = base_price * quantity
            reason = "Standard pricing"
        return {"quote": price, "reason": reason, "history": history}

class SalesAgent:
    def run(self, order: dict) -> dict:
        return tool_create_transaction(order)

class FinanceAgent:
    def run(self) -> dict:
        balance = tool_get_cash_balance()
        report = tool_generate_financial_report()
        return {"balance": balance, "report": report}

# ------------------ ORCHESTRATOR ------------------

class OrchestratorAgent:
    def handle_request(self, request: dict) -> dict:
        req_type = request.get("type")
        if req_type == "inventory":
            return InventoryAgent().run(int(request["item_id"]))
        elif req_type == "quote":
            return QuoteAgent().run(
                int(request["customer_id"]),
                int(request["item_id"]),
                int(request["quantity"])
            )
        elif req_type == "sale":
            order_str = request.get("order")
            try:
                order = ast.literal_eval(order_str) if isinstance(order_str, str) else order_str
            except Exception:
                return {"error": "Invalid order format"}
            return SalesAgent().run(order)
        elif req_type == "finance":
            return FinanceAgent().run()
        else:
            return {"error": "Unknown request type"}
