# Tool Test Prompts (V4 Agent)

This file provides a list of prompts and commands designed to test each individual tool and the various workflows implemented in the Pricing Bot V4 agent. Questions range from basic to tough, covering different scenarios.

## Section 1: Testing Individual Tools (Basic)

### `list_services`
1.  "List all services."
2.  "What services are available?"

### `list_skus_for_service`
1.  "List SKUs for BigQuery."
2.  "Show me all Cloud Storage SKUs."
3.  "Give me all SKUs for Cloud Functions."

### `list_skus_for_service_and_region`
1.  "List Compute Engine SKUs in us-east1."
2.  "Show me all Cloud SQL SKUs in europe-west3."
3.  "Show me all Google Kubernetes Engine SKUs in asia-northeast1."

### `get_sku_pricing`
1.  "What is the price of SKU 6F81-5844-456A?" (Replace with a real SKU ID from your data)
2.  "Tell me the pricing for SKU 2E27-4F75-95CD." (Replace with a real SKU ID from your data)

## Section 2: Testing Agent Workflows (Intermediate)

### Getting Pricing (Proactive Behavior)
1.  "Find a BigQuery SKU and tell me its price."
2.  "Show me an example of Cloud Storage pricing."
3.  "Give me an example of a networking SKU and its price in USD."

### Explaining Tiered Pricing
1.  "Explain the pricing tiers for Cloud Storage Standard Storage."
2.  "Is the pricing for BigQuery Analysis tiered?"
3.  "Explain the pricing tiers for Cloud Dataflow."

### Handling Currencies
1.  "What is the price of a Compute Engine n2-standard-2 instance in EUR?"
2.  "Tell me the price of a Cloud SQL MySQL instance in JPY."
3.  "What is the price of a Cloud Pub/Sub SKU in GBP?" (Test if it reports if GBP is not available and gives USD)

### Handling Committed Use Discounts (CUDs)
1.  "What is the price of a Compute Engine n2-standard-2 instance?" (Should trigger CUD hint)
2.  "Tell me about Committed Use Discounts for Cloud SQL."

## Section 3: Tougher Scenarios (Advanced)

### Finding the Cheapest SKU
1.  "Find the cheapest on-demand BigQuery storage SKU in the US."
2.  "What is the most affordable Cloud Functions SKU in us-central1?"
3.  "Find the cheapest Compute Engine vCPU SKU in europe-west1."
4.  "What is the cheapest Cloud NAT SKU in southamerica-east1?"

### Combined Workflows
1.  "Explain the tiered pricing for the cheapest Cloud Storage Nearline SKU in asia-southeast1."
2.  "What is the price of a Cloud SQL PostgreSQL instance in europe-west1 in EUR, and is it eligible for CUDs?"

### Vague/Challenging Queries
1.  "How much does it cost to store data?" (Should ask for clarification)
2.  "What's the price of a database?" (Should ask for clarification)
3.  "Tell me everything about Compute Engine pricing." (Should provide a summary and offer to list SKUs or specific pricing)
4.  "How much would it cost to run a small web server for a month in us-central1?" (Very vague, requires a lot of assumptions and clarification).
