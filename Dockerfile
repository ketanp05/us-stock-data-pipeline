FROM python:3.11.2-buster

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libssl-dev libffi-dev python3-dev && \
    apt-get install -y wget gcc && \
    apt-get clean

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Set the command to run the ingestion script
CMD ["python", "scripts/data_ingestion/alpha_vantage_ingestion.py"]
