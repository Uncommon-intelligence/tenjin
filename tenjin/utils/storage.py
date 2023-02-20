import os
import boto3
import json
from dotenv import load_dotenv

s3_endpoint_url = os.environ.get("S3_ENDPOINT_URL")
conversation_bucket = "tenjin-conversations"
s3 = boto3.client("s3", endpoint_url=s3_endpoint_url)


def store_conversation_data(file_name: str, payload: dict) -> None:
    """
    Uplods a JSON file to S3.

    Args:
        file_name (str): Name of the file to be uploaded.
        payload (dict): Data to be uploaded.

    Returns:
        None: This function does not return anything.
    """
    s3.put_object(Bucket=conversation_bucket, Key=file_name, Body=json.dumps(payload))


def fetch_conversation_data(file_name: str):
    try:
        response = s3.get_object(Bucket=conversation_bucket, Key=file_name)
        json_data = response["Body"].read().decode("utf-8")

        conversation = json.loads(json_data)
    except:
        conversation = {}

    history = conversation.get("history", [])
    buffer = conversation.get("buffer", [])

    return history, buffer