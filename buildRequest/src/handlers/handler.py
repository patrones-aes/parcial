import json
import requests
import pystache
import decimal

from src.servives.dynamoDB import getItemDynamoInvoiceStatus, getItemDynamo, putItemDynamo


def handlerEvent(event, context):
    global keyDynamo, jsonBody
    responseLa = {
        "headers": {"Content-Type": "application/json"},
        "statusCode": 200,
        "body": {},
        "isBase64Encoded": False,
    }
    print("Source event", event)

    """ Data from request """
    print("Start processing.....")
    method = event["httpMethod"]
    queryStringParameters = event["queryStringParameters"]
    body = event["body"]

    if method == "GET":
        keyDynamo = int(queryStringParameters["convenio"])
    else:
        jsonBody = json.loads(body)
        keyDynamo = jsonBody["convenio"]

        """Invoice status validation"""
        invoiceStatus = getItemDynamoInvoiceStatus(jsonBody["factura"])
        print("****", invoiceStatus)
        invoice = invoiceStatus.get("Item", None)
        if invoice is not None:
            if invoice["status"] == "in-progress":
                responseLa["body"] = json.dumps(
                    {"message": "Invoice with payment in process"}
                )
                return responseLa
            if invoice["status"] == "paid":
                responseLa["body"] = json.dumps(
                    {"message": "Invoice with payment finished"}
                )
                return responseLa

    print("Consulting provider: ", keyDynamo)
    resulDynamo = getItemDynamo(keyDynamo)
    print(resulDynamo)
    print()
    item = resulDynamo.get("Item", None)
    if item is None:
        responseLa["body"] = json.dumps(
            {"message": "Provider not found"}
        )
        return responseLa

    typeService = item["type"]
    stringTemplate = json.dumps(item, default=default_type_error_handler)

    """payment management"""
    print("method: ", method)
    print("typeService: ", typeService)
    if typeService == "REST":
        """Method == POST"""
        if method == "POST":
            putItemDynamo({"status": "in-progress", "factura": jsonBody["factura"]}, True)  #Put Item
            resultTemplate = pystache.render(stringTemplate, jsonBody)
            tempJson = json.loads(resultTemplate)
            print("requestData:\n - URL: {}\n - BODY: {}\n - HEADERS: {}\n".format(tempJson["url"], tempJson["body"],
                                                                                   tempJson["headers"]))
            result = requests.post(tempJson["url"], tempJson["body"], headers=tempJson["headers"])
            if result.status_code == 200:
                putItemDynamo({"status": "paid", "factura": jsonBody["factura"]}, False)

            responseLa["body"] = json.dumps(json.loads(result.text))

        if method == "GET":
            resultTemplate = pystache.render(stringTemplate, queryStringParameters)
            tempJson = json.loads(resultTemplate)
            print("requestData:\n - URL: {}\n - queryStringParameters: {}\n - HEADERS: {}\n".format(tempJson["url"],
                                                                                                    tempJson[
                                                                                                        "queries_params"],
                                                                                                    tempJson[
                                                                                                        "headers"]))
            result = requests.get(tempJson["url"], json.loads(tempJson["queries_params"]), headers=tempJson["headers"])
            print(result.request.url)
            responseLa["body"] = json.dumps(json.loads(result.text))

    elif typeService == "SOAP":
        responseLa["headers"] = {"Content-Type": "text/xml"}
        if method == "POST":
            putItemDynamo({"status": "in-progress", "factura": jsonBody["factura"]}, True)  # Put Item
            resultTemplate = pystache.render(stringTemplate, jsonBody)
            tempJson = json.loads(resultTemplate)
            print("requestData:\n - URL: {}\n - BODY: {}\n - HEADERS: {}\n".format(tempJson["url"],
                                                                                   tempJson["bodyPayBill"],
                                                                                   tempJson["headers"]))
            result = requests.post(tempJson["url"], tempJson["bodyPayBill"], headers=tempJson["headers"])
            if result.status_code == 200:
                putItemDynamo({"status": "paid", "factura": jsonBody["factura"]}, False)

            responseLa["body"] = result.text

        if method == "GET":
            resultTemplate = pystache.render(stringTemplate, queryStringParameters)
            tempJson = json.loads(resultTemplate)
            print("requestData:\n - URL: {}\n - bodyCkeckBill: {}\n - HEADERS: {}\n".format(tempJson["url"],
                                                                                            tempJson[
                                                                                                "bodyCkeckBill"],
                                                                                            tempJson[
                                                                                                "headers"]))
            result = requests.post(tempJson["url"], tempJson["bodyCkeckBill"], headers=tempJson["headers"])
            print(result.text)
            responseLa["body"] = result.text

    return responseLa


def default_type_error_handler(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError


"""
        1. Si la solicitud del api es de tipo get y el convenio en tipo soap, se envian los queries_params
        2. Si la solicitud del api es de tipo post y el convenio en tipo soap, se envía el body en xml
"""
""" Contrato de entrada
        {
            "factura":1002568415,
            "convenio":100
        }
"""


"""def test():
    event = {
        'httpMethod': 'POST',
        'body': '{"factura": 1002568415,"convenio": 100,"cliente":"jesus velasquez","id":1047, "valor":100000}',
        'queryStringParameters': {'convenio': '100', 'factura': '100555555'},
    }
    print(handlerEvent(event, ""))


test()"""
