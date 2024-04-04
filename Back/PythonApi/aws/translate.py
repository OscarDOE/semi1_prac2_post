import boto3

from aws.env import *

def translate_text(text_to_translate, lang):
    # Create an AWS Translate client
    translate_client = boto3.client('translate',
        aws_access_key_id=AWS_ACCESS_TRANSLATE,
        aws_secret_access_key=AWS_SECRET_TRANSLATE,
        region_name=REGION_NAME_TRANSLATE)

    # Source language of the text
    source_language = "es"

    # Target languages for translation
    target_languages = ["en", "ja", "fr"]

    # Dictionary to store translations
    translations = {}

    for target_language in target_languages:
        # Perform translation
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )

        # Get the translated text
        translated_text = response['TranslatedText']

        # Store the translation in the dictionary
        translations[target_language] = translated_text

    return translations