import requests
from bs4 import BeautifulSoup
import boto3
import uuid
import os

def lambda_handler(event, context):
    url = "https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados"

    response = requests.get(url)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': 'Error al acceder a la página del IGP'
        }

    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla principal
    table = soup.find('table')
    if not table:
        return {
            'statusCode': 404,
            'body': 'No se encontró la tabla de sismos'
        }

    # Extraer headers
    headers = [th.text.strip() for th in table.find_all('th')]

    # Extraer filas (solo los primeros 10 sismos)
    rows = []
    for tr in table.find_all('tr')[1:11]:  # saltamos header, tomamos 10
        tds = tr.find_all('td')
        row = {headers[i]: tds[i].text.strip() for i in range(len(tds))}
        rows.append(row)

    # Solo imprimimos por ahora
    print("=== Últimos 10 sismos IGP ===")
    for r in rows:
        print(r)

    # Si luego deseas almacenar, habilita esto 👇
    """
    dynamo = boto3.resource('dynamodb')
    table_name = os.environ["TABLE_NAME"]
    table = dynamo.Table(table_name)

    for r in rows:
        r["id"] = str(uuid.uuid4())
        table.put_item(Item=r)
    """

    return {
        "statusCode": 200,
        "body": "ya se hizo el scraping!!"
    }
