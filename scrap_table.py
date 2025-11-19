import requests
import boto3
import uuid
import os

def lambda_handler(event, context):
    # URL oficial del IGP para sismos del año actual (2025)
    url = "https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/2025"

    response = requests.get(url)
    if response.status_code != 200:
        return {
            "statusCode": response.status_code,
            "body": "Error al acceder a la API del IGP"
        }

    data = response.json()

    # DEBUG opcional
    print("=== Datos recibidos del IGP ===")
    print(f"Cantidad: {len(data)} sismos")

    # DynamoDB
    dynamo = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]  # <=== usa TABLE_NAME del serverless.yml
    table = dynamo.Table(table_name)

    # Guardar cada sismo en DynamoDB
    for sismo in data:
        item = sismo.copy()
        item["id"] = str(uuid.uuid4())  # id único para la tabla

        # Insertar en DynamoDB
        table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": f"Se almacenaron {len(data)} sismos del IGP exitosamente."
    }
