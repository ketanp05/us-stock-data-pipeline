# US Stock Data Pipeline

This project ingests, processes, and analyses financial data from US stock exchange using AWS services. The architecture is designed to be scalable and resilient.

## Project Structure

- **dags/**: Contains Airflow DAGs.
- **infrastructure/terraform**: Terraform scripts for infrastructure provisioning.
- **scripts/**: Data ingestion, transformation, and web scraping scripts.
- **notebooks/**: Jupyter notebooks for data analysis.
- **src/**: Utility functions and main entry point of the project.
- **tests/**: Unit tests.
- **Dockerfile**: Docker setup.
- **docker-compose.yml**: Docker compose setup.
- **requirements.txt**: Project dependencies.

## Getting Started

1. Clone the repository.
2. Set up AWS credentials.
3. Use Terraform to provision infrastructure.
4. Run data ingestion scripts.
5. Analyse data using Jupyter notebooks.