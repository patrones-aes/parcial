# PATRONES DE ARQUITECTURA
### AES- Especialización en Arquitectura Empresarial y Software
#### Pontificia Universidad Javeriana - Bogota D.C

# Introducción
Este proyecto se implementó dando foco al atributo de calidad de **Modicaficabilidad** identificado en el
enuciado del problema: 
**"El Banco ABC quiere tener la posibilidad de adicionar nuevos convenios con otros proveedores
de servicios de manera ágil, o incluso la posibilidad de terminar/eliminar los convenios
existentes sin que esto represente indisponibilidad del servicio.
Se llegó a un acuerdo de las capacidades/primitivas básicas que se deben soportar para cada
convenio:**

● **Consulta de saldo a Pagar**

● **Pago del Servicio**

● **Compensación de pago (Opcional)**

**Principalmente el banco necesita un conjunto de servicios de integración que representen sus
necesidades internas de negocio, lo cual les permite desacoplar los servicios de los
proveedores y así no depender de sus detalles."**

# Consideraciones
Bajo los supuestos de que el Banco ABC quiere empezar a explorar soluciones en la nube, se diseña
y crea una solución basada en AWS como proveedor Cloud, a continución se muestra el diagrama
de despliegue:
![image](https://github.com/patrones-aes/parcial/assets/24567258/dcce9e74-9c4b-47f8-9a19-b6fefedbf15e)


# Despliegue
Para desplegar este servicio debe:
1. Clonar el repositorio a un enterno local.
2. Compilar un .zip python con dependecias, para lo cual puede seguir la instrucciones del 
siguiente link: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html.
3. Tener una creada una cuenta de AWS o crearla desde 0.
4. Desde la consola de AWS crear lo siguientes recursos:

    * Apigategay de tipo REST
    * Lambda (Nombre personalizado o utilizar el dado en el digrama)
    * 2 tablas en dynamo:  1 para los proveedores con replica en la zona deseada, en este caso en
   ohio y replica en Norte de Virginia y la otra es para la persistencia y gestion de los mensages.

   Nota: Los recursos creados deben tener los permisos requeridos para su correcto funcionamiento
    por ejemplo, las lambdas deben porder leer y escribir en las tabls de dynamo
5. Desplegar el .zip de la lambda en AWS.

El siguiente bloque de código puede ser utilizado para aprobicionar el APiGategay en aws,
remplazando los valores:

+ API_ID
+ ACCOUNT_ID
+ LAMBDA_NAME


```json
{
  "swagger" : "2.0",
  "info" : {
    "description" : "Prueba",
    "version" : "2024-05-27T21:49:19Z",
    "title" : "bancoABC"
  },
  "host" : "API_ID.execute-api.us-east-2.amazonaws.com",
  "basePath" : "/dev",
  "schemes" : [ "https" ],
  "paths" : {
    "/bill" : {
      "get" : {
        "produces" : [ "application/json" ],
        "responses" : {
          "200" : {
            "description" : "200 response",
            "schema" : {
              "$ref" : "#/definitions/Empty"
            }
          }
        },
        "x-amazon-apigateway-integration" : {
          "httpMethod" : "POST",
          "uri" : "arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-2:ACCOUNT_ID:function:LAMBDA_NAME/invocations",
          "responses" : {
            "default" : {
              "statusCode" : "200"
            }
          },
          "passthroughBehavior" : "when_no_match",
          "contentHandling" : "CONVERT_TO_TEXT",
          "type" : "aws_proxy"
        }
      },
      "post" : {
        "produces" : [ "application/json" ],
        "responses" : {
          "200" : {
            "description" : "200 response",
            "schema" : {
              "$ref" : "#/definitions/Empty"
            }
          }
        },
        "x-amazon-apigateway-integration" : {
          "httpMethod" : "POST",
          "uri" : "arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-2:ACCOUNT_ID:function:LAMBDA_NAME/invocations",
          "responses" : {
            "default" : {
              "statusCode" : "200"
            }
          },
          "passthroughBehavior" : "when_no_match",
          "contentHandling" : "CONVERT_TO_TEXT",
          "type" : "aws_proxy"
        }
      },
      "options" : {
        "consumes" : [ "application/json" ],
        "produces" : [ "application/json" ],
        "responses" : {
          "200" : {
            "description" : "200 response",
            "schema" : {
              "$ref" : "#/definitions/Empty"
            }
          }
        },
        "x-amazon-apigateway-integration" : {
          "responses" : {
            "default" : {
              "statusCode" : "200"
            }
          },
          "requestTemplates" : {
            "application/json" : "{\"statusCode\": 200}"
          },
          "passthroughBehavior" : "when_no_match",
          "type" : "mock"
        }
      }
    }
  },
  "definitions" : {
    "Empty" : {
      "type" : "object",
      "title" : "Empty Schema"
    }
  }
}
```
Al seguir los pasos anteriores, tendremos listo nuestro servicio para ser probado.

# Uso
