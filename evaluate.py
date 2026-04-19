# evaluate.py
import csv
from beaver_agents import OrchestratorAgent

def evaluate_system(input_csv: str, output_csv: str):
    orchestrator = OrchestratorAgent()
    results = []

    with open(input_csv, newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                response = orchestrator.handle_request(row)
                results.append({
                    "Request": row,
                    "Outcome": response.get("status") or response.get("quote") or response.get("balance") or "N/A",
                    "Reason": response.get("reason") or response.get("delivery") or response.get("report", {}).get("summary") or response.get("error") or "N/A",
                    "Cash Balance Change": response.get("report", {}).get("cash_change", "N/A")
                })
            except Exception as e:
                results.append({
                    "Request": row,
                    "Outcome": "Error",
                    "Reason": str(e),
                    "Cash Balance Change": "N/A"
                })

    with open(output_csv, "w", newline="") as outfile:
        fieldnames = ["Request", "Outcome", "Reason", "Cash Balance Change"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

if __name__ == "__main__":
    evaluate_system("quote_requests_sample.csv", "test_results.csv")
    print("Evaluation complete. Results written to test_results.csv")