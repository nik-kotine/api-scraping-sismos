import os
import uuid
import boto3
from playwright.sync_api import sync_playwright

def lambda_handler(event, context):

    # Iniciar DynamoDB
    dynamo = boto3.resource("dynamodb")
    table = dynamo.Table(os.environ["TABLE_NAME"])

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ])
        page = browser.new_page()

        url = "https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados"
        page.goto(url, wait_until="networkidle")

        # Esperar tabla
        page.wait_for_selector("table")

        # Extraer filas
        filas = page.query_selector_all("table tbody tr")

        sismos = []

        for tr in filas[:10]:  # solo los 10 últimos
            tds = tr.query_selector_all("td")
            cols = [c.inner_text().strip() for c in tds]

            # Cada fila tiene ~10 columnas; las guardamos genéricamente
            item = {
                "id": str(uuid.uuid4()),
                "fecha": cols[0],
                "hora": cols[1],
                "magnitud": cols[2],
                "profundidad": cols[3],
                "latitud": cols[4],
                "longitud": cols[5],
                "referencia": cols[6],
            }

            sismos.append(item)

            # Guardar en DynamoDB
            table.put_item(Item=item)

        browser.close()

    return {
        "statusCode": 200,
        "body": f"Guardados {len(sismos)} sismos del IGP usando PLAYWRIGHT."
    }
