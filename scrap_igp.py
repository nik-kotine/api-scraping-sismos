import requests
import boto3
import uuid
import os

def lambda_handler(event, context):
    url = "https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/2025"
    response = requests.get(url)
    if response.status_code != 200:
        return { "statusCode": response.status_code, "body": "Error al acceder a la API del IGP" }
    data = response.json()
    dynamo = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamo.Table(table_name)
    for sismo in data:
        item = sismo.copy()
        item["id"] = str(uuid.uuid4())
        table.put_item(Item=item)
    return {
        "statusCode": 200,
        "body": f"Se almacenaron {len(data)} sismos del IGP exitosamente."
    }