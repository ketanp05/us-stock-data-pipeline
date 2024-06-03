"""
Ingest data from the Alpha Vantage API and store it in AWS S3.
"""

import os
import requests
import pandas as pd
import boto3
from botocore.exceptions import ClientError

# set up environment variables
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_REGION
)

def fetch_alpha_vantage_data(symbol, function='TIME_SERIES_DAILY'):
    """
    Fetches data from Alpha Vantage API.

    args:
    symbol[string] - stock
    function[string] - type of data

    returns:
    data[dict]
    """
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'Error Message' in data:
        raise ValueError(f"Error fetching data for symbol {symbol}: {data['Error Message']}")

    return data

def transform_data_to_dataframe(data):
    """
    Transform JSON data to Pandas dataframe

    args:
    data[dict] - data fetched from alpha vantage in json
    """
    time_series = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns = lambda x:x.split(' ')[1])
    return df

def upload_to_s3(dataframe, symbol, bucket, object_name):
    """
    uploads dataframe to s3
    """
    csv_buffer = dataframe.to_csv()
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer)
        print(f"Successfully uploaded {object_name} to {bucket}")
    except ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            print("Access denied! Check your credentials or permissions.")
        elif error.response['Error']['Code'] == 'NoSuchBucket':
            print(f"Bucket '{bucket_name}' does not exist.")
        else:
            print(f"Unexpected error: {error}")

def main():
    symbols = ['AAPL', 'MSFT', 'GOOGL']

    for symbol in symbols:
        print(f"Fetching data for {symbol}")
        data = fetch_alpha_vantage_data(symbol)
        df = transform_data_to_dataframe(data)
        object_name = f"data/raw/{symbol}.csv"
        upload_to_s3(df, symbol, S3_BUCKET_NAME, object_name)

if __name__ == "__main__":
    main()
