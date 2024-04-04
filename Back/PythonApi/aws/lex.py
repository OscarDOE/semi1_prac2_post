import boto3

from env import *

def send_message_lex(message, session_id):
    # Detalles de la solicitud
    bot_id = 'SXMI900ZIY'
    bot_alias_id = 'TSTALIASID'

    try:
        lex_client = boto3.client('lexv2-runtime',
                                  AWS_ACCESS_LEX=AWS_ACCESS_LEX,
                                  aws_secret_access_key=AWS_SECRET_LEX,
                                  region_name=REGION_NAME_LEX
                )
        response = lex_client.recognize_text(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId="es_ES",  # Especifica el idioma si es diferente
            sessionId=session_id,
            text=message
        )
        return response['messages']

    except:
        return None