from src.handlers.handler import handlerEvent


def start(event, context):
    return handlerEvent(event, context)
