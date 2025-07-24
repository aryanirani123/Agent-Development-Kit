# Agent Development Kit (ADK) - Sample Agents

This repository contains a collection of sample agents built using the Google Agent Development Kit (ADK). Each agent demonstrates different features and capabilities of the ADK, from simple instruction-based agents to more complex agents that integrate with external tools and services.

## Agents

Here is a list of the agents included in this repository:

1.  **Helpful Assistant**
2.  **Google Search Agent**
3.  **Travel Planner Agent**
4.  **Google Tasks Agent**
5.  **Invoice Tracker Agent**
6.  **Grounded Agent (GCP Release Notes)**
7.  **Retail Operations Agent**
8.  **Inventory Management Agent**

---

### 1. Helpful Assistant

*   **File:** `1 - Helpful-Assistant/agent.py`
*   **Description:** This is a basic conversational agent that answers questions about a developer talk on Agent Development Kits (ADK). It's a simple, instruction-based agent that doesn't use any external tools.
*   **Model:** `gemini-2.0-flash-001`

---

### 2. Google Search Agent

*   **File:** `2 - Google-Search-Agent/agent.py`
*   **Description:** This agent can answer questions by searching the internet using the built-in `google_search` tool.
*   **Model:** `gemini-2.0-flash`
*   **Tools:** `google_search`

---

### 3. Travel Planner Agent

*   **File:** `3 - Travel-Planner-Agent/agent.py`
*   **Description:** A helpful agent to assist users with their travel planning.
*   **Model:** `gemini-2.0-flash-001`

---

### 4. Google Tasks Agent

*   **File:** `4 - Google-Tasks-Agent/agent.py`
*   **Description:** A conversational agent that manages a to-do list using the Google Tasks API. It can add, list, and complete tasks.
*   **Model:** `gemini-2.0-flash-001`
*   **Tools:** `list_tasks`, `add_task`, `complete_task`
*   **Setup:** Requires `credentials.json` from the Google Cloud Console with the Google Tasks API enabled.

---

### 5. Invoice Tracker Agent

*   **File:** `5 - Invoice-Tracker-Agent/agent.py`
*   **Description:** Extracts structured invoice data from image files using Gemini.
*   **Model:** `gemini-2.5-flash-preview-04-17`
*   **Tools:** `extract_invoice_details`
*   **Setup:** Requires a `.env` file with your `MODEL` if you want to override the default.

---

### 6. Grounded Agent (GCP Release Notes)

*   **Files:** `6 - Grounded-Agent/agent.py`, `6 - Grounded-Agent/tools.yaml`
*   **Description:** An agent that answers questions about Google Cloud Release notes by querying a BigQuery dataset.
*   **Model:** `gemini-2.0-flash`
*   **Tools:** `search_release_notes_bq` (defined in `tools.yaml`)
*   **Setup:** This agent uses `toolbox-core` to connect to a local toolbox server. It also requires a BigQuery project and dataset.

---

### 7. Retail Operations Agent

*   **Files:** `7 - Retails-Operations-Agent/agent.py`, `7 - Retails-Operations-Agent/tools.yaml`
*   **Description:** A smart sales analytics assistant that uses BigQuery to explore sales performance across products, cities, stores, and salespeople.
*   **Model:** `gemini-2.0-flash`
*   **Tools:** `top_selling_products_by_store`, `daily_sales_summary` (defined in `tools.yaml`)
*   **Setup:** This agent uses `toolbox-core` to connect to a local toolbox server. It also requires a BigQuery project and dataset.

---

### 8. Inventory Management Agent

*   **Files:** `8 - Inventory-Management-Agent/agent.py`, `8 - Inventory-Management-Agent/tools.yaml`
*   **Description:** An inventory co-pilot to check stock levels, generate low-stock reports, and find the top-selling product of the week using BigQuery.
*   **Model:** `gemini-2.0-flash`
*   **Tools:** `fetch_stock_for_product`, `get_low_stock_items`, `most_ordered_product_this_week` (defined in `tools.yaml`)
*   **Setup:** This agent uses `toolbox-core` to connect to a local toolbox server. It also requires a BigQuery project and dataset.
