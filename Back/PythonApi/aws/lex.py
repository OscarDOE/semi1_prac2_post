import boto3

from aws.env import *

def send_message_lex(message, session_id):
    # Detalles de la solicitud
    bot_id = BOTID
    bot_alias_id = BOTALIASID
    print("BOT")

    try:
        print("BOT  TRY")
        lex_client = boto3.client('lexv2-runtime',
                                  aws_access_key_id=AWS_ACCESS_LEX,
                                  aws_secret_access_key=AWS_SECRET_LEX,
                                  region_name=REGION_NAME_LEX
                )
        print("reponse antes")
        response = lex_client.recognize_text(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId="es_ES",  # Especifica el idioma si es diferente
            sessionId=session_id,
            text=message
        )
        print("reponse", response)
        return response['messages']

    except:
        print("EXCEPT")
        return None