import pandas as pd
import time
from sqlalchemy import create_engine

from project_starter import init_database, generate_financial_report
from beaver_agents import OrchestratorAgent


def run_test_scenarios():

    print("Initializing Database...")

    engine = create_engine("sqlite:///munder_difflin.db")
    init_database(engine)

    orchestrator = OrchestratorAgent(engine)

    # ---------------------------
    # LOAD CSV
    # ---------------------------
    try:
        df = pd.read_csv(
            "quote_requests_sample.csv",
            engine="python",
            on_bad_lines="skip"
        )

        df.columns = df.columns.str.strip().str.lower()

        required_cols = ["type", "customer_id", "item_id", "quantity", "price"]

        for col in required_cols:
            if col not in df.columns:
                raise Exception(f"Missing column: {col}")

        # create safe date column
        df["request_date"] = pd.date_range(
            start="2024-01-01",
            periods=len(df),
            freq="D"
        )

    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return

    # ---------------------------
    # INITIAL STATE
    # ---------------------------
    initial_date = df["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)

    current_cash = report.get("cash_balance", 0)
    current_inventory = report.get("inventory_value", 0)

    results = []

    # ---------------------------
    # MAIN LOOP
    # ---------------------------
    for idx, row in df.iterrows():

        request_date = row["request_date"].strftime("%Y-%m-%d")

        print(f"\n=== Request {idx+1} ===")
        print(f"Type: {row['type']}")
        print(f"Customer: {row['customer_id']}")
        print(f"Item: {row['item_id']}")
        print(f"Quantity: {row['quantity']}")

        # ---------------------------
        # BUILD REQUEST
        # ---------------------------
        # ---------------------------
# BUILD REQUEST SAFELY
# ---------------------------
        if row["type"] == "quote":
            structured_request = {
                "type": "quote",
                "customer_id": int(row["customer_id"]),
                "item_id": int(row["item_id"]),
                "quantity": int(row["quantity"])
                }
        elif row["type"] == "sale":
            structured_request = {
                "type": "sale",
                "order": {
                    "customer_id": int(row["customer_id"]),
                    "item_id": int(row["item_id"]),
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"])
                    }
                }

        elif row["type"] == "sale":
            structured_request = {
                "type": "sale",
                "order": {
                    "customer_id": int(row["customer_id"]),
                    "item_id": int(row["item_id"]),
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"])
                }
            }

        elif row["type"] == "inventory":
            structured_request = {
                "type": "inventory",
                "item_id": int(row["item_id"]) if pd.notna(row["item_id"]) else 101
            }

        elif row["type"] == "finance":
            structured_request = {
                "type": "finance"
            }

        else:
            structured_request = {
                "type": "inventory",
                "item_id": 101
            }

        # ---------------------------
        # AGENT CALL
        # ---------------------------
        response = orchestrator.handle_request(structured_request)

        # update state
        report = generate_financial_report(request_date)
        current_cash = report.get("cash_balance", 0)
        current_inventory = report.get("inventory_value", 0)

        print(f"Response: {response}")
        print(f"Cash: ${current_cash:.2f} | Inventory: ${current_inventory:.2f}")

        results.append({
            "request_id": idx + 1,
            "request_date": request_date,
            "response": str(response)
        })

        time.sleep(1)

    print("\n===== FINAL REPORT =====")

    final_date = df["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)

    print(f"Final Cash: ${final_report.get('cash_balance', 0):.2f}")
    print(f"Final Inventory: ${final_report.get('inventory_value', 0):.2f}")

    pd.DataFrame(results).to_csv("test_results.csv", index=False)

    return results


if __name__ == "__main__":
    run_test_scenarios()