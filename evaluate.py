# evaluate.py
# Evaluation script for Beaver's Choice Paper Company multi-agent system
# Runs all 19 requests from quote_requests_sample.csv and logs results

import csv
from beaver_agents import OrchestratorAgent

def evaluate_system(input_csv: str, output_csv: str):
    orchestrator = OrchestratorAgent()
    results = []

    # Read all requests from the provided dataset
    with open(input_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Each row should contain fields like: type, action, paper_type, quantity, price, customer_id, item_id, order
            request = {
                "type": row.get("type"),
                "action": row.get("action"),
                "paper_type": row.get("paper_type"),
                "quantity": int(row.get("quantity")) if row.get("quantity") else None,
                "price": float(row.get("price")) if row.get("price") else None,
                "customer_id": int(row.get("customer_id")) if row.get("customer_id") else None,
                "item_id": int(row.get("item_id")) if row.get("item_id") else None,
                "order": row.get("order")
            }
            response = orchestrator.handle_request(request)
            results.append({
                "Request": str(request),
                "Outcome": str(response),
                "Reason": response.get("reason", "N/A") if isinstance(response, dict) else "N/A",
                "Cash Balance Change": "Yes" if isinstance(response, dict) and "balance" in response else "No"
            })

    # Save results to test_results.csv
    with open(output_csv, "w", newline='') as csvfile:
        fieldnames = ["Request", "Outcome", "Reason", "Cash Balance Change"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

if __name__ == "__main__":
    # Run evaluation on the full dataset
    evaluate_system("quote_requests_sample.csv", "test_results.csv")
    print("Evaluation complete. Results saved to test_results.csv")
