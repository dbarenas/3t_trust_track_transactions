# Financial Transaction Analysis System

## Overview

This project is a Minimum Viable Product (MVP) of a financial transaction analysis system designed for expenditure traceability and basic detection of Anti-Money Laundering (AML) and corruption activities. The system's core feature is a simulated in-memory blockchain that serves as the single, immutable source of truth for all financial records, ensuring data integrity and auditability.

A key regulatory requirement implemented in this system is that all transactions exceeding a 500 USD/EUR threshold must be accompanied by an `AssetValuation` record, which is also stored and certified on the blockchain.

## Architecture

The system follows a modular architecture, with a clear separation of concerns to promote maintainability and extensibility. The data flow is as follows:

`Raw Data -> Ingestion & Cleaning -> Transaction & Valuation Objects -> Blockchain (Blocks) -> AML & Reputation Analysis -> Alerts`

All analytical tasks, including AML checks and reputation scoring, are performed by reading data directly from the blockchain, reinforcing its role as the single source of truth.

## Core Features

- **Simulated Blockchain:** An in-memory blockchain that stores all transactions and asset valuations, ensuring immutability.
- **Data Ingestion and Cleaning:** A pipeline to process raw data, clean it, and convert it into structured Pydantic models.
- **On-Chain Valuation:** A mechanism to enforce the requirement that all transactions over 500 USD/EUR have a corresponding `AssetValuation` record on the blockchain.
- **AML Rules Engine:** A set of rules to detect suspicious activities, including:
  - High-value transactions lacking the required on-chain valuation.
  - Transactions involving blacklisted entities.
  - Transaction splitting (Fraccionamiento) to circumvent value thresholds.
  - Circular fund flows (e.g., A -> B -> C -> A).
- **Reputation System:** A scoring system to assess the risk profile of entities based on their transaction history.
- **Alerting System:** A mechanism to generate alerts when suspicious activities are detected.
- **Comprehensive Test Suite:** A suite of tests written with `pytest` to ensure the correctness and robustness of the system.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file from the installed packages: `pip freeze > requirements.txt`)*

## Usage

To run the main application and see a demonstration of the system's capabilities, execute the following command from the root of the project:

```bash
python -m src.main
```

The script will:
1.  Generate synthetic "good" and "suspicious" transaction data.
2.  Process the data through the ingestion pipeline.
3.  Build the blockchain with the transactions and valuations.
4.  Run the AML and reputation analysis.
5.  Print a summary of the results, including the blockchain's validity, any generated AML alerts, and the calculated reputation scores.

## Testing

To run the full suite of tests, use `pytest`:

```bash
pytest
```

The tests cover the integrity of the blockchain, the logic of the AML rules, the valuation system, and the reputation scoring.

## Future Extensibility

This MVP is designed to be extensible. Potential future enhancements include:

- **Persistence:** Integrating a database or distributed ledger to persist the blockchain data.
- **Real Blockchain Integration:** Connecting the system to a real blockchain network.
- **Advanced AML Rules:** Incorporating more sophisticated machine learning models for risk scoring and anomaly detection.
- **Cryptographic Signatures:** Implementing real digital signatures for asset valuations to enhance security.
- **REST API:** Exposing the system's functionalities through a REST API for real-time queries and analysis.
