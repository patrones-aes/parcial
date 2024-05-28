import boto3
from datetime import datetime, timedelta

s3 = boto3.client("s3", region_name="us-east-2")
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")


def getItemDynamo(cod_proveedor):
    table = dynamodb.Table("Proveedores")
    response = table.get_item(Key={"cod_proveedor": cod_proveedor})
    return response


def getItemDynamoInvoiceStatus(cod_proveedor):
    table = dynamodb.Table("registroTrans")
    response = table.get_item(Key={"nro_invoice": cod_proveedor})
    return response


def putItemDynamo(data, isttl):
    current_time = int(datetime.now().timestamp())

    expiration_time = ""
    if isttl:
        expiration_time = int((datetime.now() + timedelta(minutes=5)).timestamp())

    print("expiration_time ", expiration_time)
    table = dynamodb.Table("registroTrans")
    response = table.put_item(Item={
        "nro_invoice": data["factura"],
        "createAT": current_time,
        "status": data["status"],
        "TTL": expiration_time
    })
    return response
