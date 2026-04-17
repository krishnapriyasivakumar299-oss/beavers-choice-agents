{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOliL5uAohLyY0+WanRFHh9",
      "include_colab_link": True
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/krishnapriyasivakumar299-oss/beavers-choice-agents/blob/main/beaver_agents.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "E9eUfBhCe276",
        "outputId": "7880c542-7ca0-4af7-804c-a6045d0ee8bd"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "{'request': 'A4 paper 500 units', 'inventory': 'Stock available: 200', 'quote': 'Price: 4500.0 (discount 10.0%)', 'sale': 'Order failed: insufficient stock', 'finance': 'Current balance: 50000'}\n"
          ]
        }
      ],
      "source": [
        "import csv\n",
        "\n",
        "# ---------------------------\n",
        "# MOCK FUNCTIONS (replace later if you have project_starter.py)\n",
        "# ---------------------------\n",
        "\n",
        "def get_stock_level(product):\n",
        "    return 200\n",
        "\n",
        "def search_quote_history(product):\n",
        "    return \"Previous price: 10 per unit\"\n",
        "\n",
        "def create_transaction(product, quantity, price):\n",
        "    return \"Transaction successful\"\n",
        "\n",
        "def get_cash_balance():\n",
        "    return 50000\n",
        "\n",
        "def extract_quantity(request):\n",
        "    words = request.split()\n",
        "    for word in words:\n",
        "        if word.isdigit():\n",
        "            return int(word)\n",
        "    return 0\n",
        "\n",
        "\n",
        "# ---------------------------\n",
        "# AGENTS (Simple Python)\n",
        "# ---------------------------\n",
        "\n",
        "class InventoryAgent:\n",
        "    def run(self, request):\n",
        "        return f\"Stock available: {get_stock_level(request)}\"\n",
        "\n",
        "\n",
        "class QuoteAgent:\n",
        "    def run(self, request):\n",
        "        quantity = extract_quantity(request)\n",
        "        price_per_unit = 10\n",
        "\n",
        "        if quantity > 100:\n",
        "            discount = 0.1\n",
        "        else:\n",
        "            discount = 0\n",
        "\n",
        "        total = quantity * price_per_unit * (1 - discount)\n",
        "\n",
        "        return f\"Price: {total} (discount {discount*100}%)\"\n",
        "\n",
        "\n",
        "class SalesAgent:\n",
        "    def run(self, request, stock):\n",
        "        quantity = extract_quantity(request)\n",
        "\n",
        "        if quantity > stock:\n",
        "            return \"Order failed: insufficient stock\"\n",
        "        return \"Transaction successful\"\n",
        "\n",
        "\n",
        "class FinanceAgent:\n",
        "    def run(self):\n",
        "        return f\"Current balance: {get_cash_balance()}\"\n",
        "\n",
        "\n",
        "# ---------------------------\n",
        "# ORCHESTRATOR\n",
        "# ---------------------------\n",
        "\n",
        "def handle_request(request):\n",
        "    quantity = extract_quantity(request)\n",
        "\n",
        "    stock = get_stock_level(request)\n",
        "\n",
        "    inventory = f\"Stock available: {stock}\"\n",
        "    quote = QuoteAgent().run(request)\n",
        "    sale = SalesAgent().run(request, stock)\n",
        "    finance = FinanceAgent().run()\n",
        "\n",
        "    return {\n",
        "        \"request\": request,\n",
        "        \"inventory\": inventory,\n",
        "        \"quote\": quote,\n",
        "        \"sale\": sale,\n",
        "        \"finance\": finance\n",
        "    }\n",
        "\n",
        "# ---------------------------\n",
        "# TEST RUN\n",
        "# ---------------------------\n",
        "\n",
        "result = handle_request(\"A4 paper 500 units\")\n",
        "print(result)\n",
        "\n",
        "def run_tests():\n",
        "    results = []\n",
        "\n",
        "    with open(\"quote_requests_sample.csv\") as f:\n",
        "        reader = csv.DictReader(f)\n",
        "\n",
        "        for row in reader:\n",
        "            request = str(row)\n",
        "            response = handle_request(request)\n",
        "\n",
        "            results.append([\n",
        "                request,\n",
        "                response[\"inventory\"],\n",
        "                response[\"quote\"],\n",
        "                response[\"sale\"],\n",
        "                response[\"finance\"]\n",
        "            ])\n",
        "\n",
        "    # Save to CSV\n",
        "    with open(\"test_results.csv\", \"w\", newline=\"\") as f:\n",
        "        writer = csv.writer(f)\n",
        "\n",
        "        writer.writerow([\n",
        "            \"request\",\n",
        "            \"inventory\",\n",
        "            \"quote\",\n",
        "            \"sale\",\n",
        "            \"finance\"\n",
        "        ])\n",
        "\n",
        "        writer.writerows(results)\n",
        "\n",
        "    print(\"✅ test_results.csv generated!\")"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# New Section"
      ],
      "metadata": {
        "id": "L7mGByjsrTed"
      }
    }
  ]
}
if __name__ == "__main__":
    print("Running test...")

    result = handle_request("A4 paper 500 units")
    print(result)
