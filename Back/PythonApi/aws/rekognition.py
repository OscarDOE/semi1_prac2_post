import boto3
from aws.env import *


# Instancia de rekognition
rekognition = boto3.client('rekognition',  aws_access_key_id=AWS_ACCESS_REKOGNITION,
        aws_secret_access_key=AWS_SECRET_REKOGNITION,
        region_name=REGION_NAME_REKOGNITION)

def detect_features_in_image(image_bytes):
    # Llamar a DetectLabels
    response = rekognition.detect_labels(
        Image={
            'Bytes': image_bytes
        }
    )

    # Extraer etiquetas detectadas
    detected_features = []
    # print("REKOG LABERS : ",response)
    for label in response['Labels']:
        detected_features.append(label['Name'])

    return detected_features

def detect_features_in_image_login(image_bytes):
    # Llamar a DetectLabels
    response = rekognition.detect_labels(
        Image={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': image_bytes
                }
            }
    )

    # Extraer etiquetas detectadas
    detected_features = []
    # print("REKOG LABERS : ",response)
    for label in response['Labels']:
        detected_features.append(label['Name'])

    return detected_features

# Comparar Rostros
def compare_images(profile_picture_key: str, webcam_image: bytes):
    print("COMPARE")

    response = rekognition.compare_faces(
        SourceImage={
            'Bytes': webcam_image
        },
        TargetImage={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': profile_picture_key
            }
        },
        SimilarityThreshold=80
    )

    print(len(response['FaceMatches']))
    if len(response['FaceMatches']) > 0:
        return response['FaceMatches'][0]['Similarity']
    else:
        return 0.0



def fatial_analisis(image):
    try:
        # print(image)
        response = rekognition.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': image
                }
            },
            Attributes=['ALL'] 
        )
        caracteristicas = []
        if response['FaceDetails']:
            for rostro in response['FaceDetails']:
                emociones = [emocion['Type'] for emocion in rostro['Emotions']]
                edad = "Edad: {}-{}".format(rostro['AgeRange']['Low'], rostro['AgeRange']['High'])
                genero = rostro['Gender']['Value']
                sonrisa = "Sonrisa: {}".format(rostro['Smile']['Value'])
                gafas = "Gafas: {}".format(rostro['Eyeglasses']['Value'])
                lentes_sol = "Lentes de sol: {}".format(rostro['Sunglasses']['Value'])
                barba = "Barba: {}".format(rostro['Beard']['Value'])
                bigote = "Bigote: {}".format(rostro['Mustache']['Value'])
                ojos_abiertos = "Ojos abiertos: {}".format(rostro['EyesOpen']['Value'])
                boca_abierta = "Boca abierta: {}".format(rostro['MouthOpen']['Value'])
                
                caracteristicas.extend(emociones + [edad, genero, sonrisa, gafas, lentes_sol, barba, bigote, ojos_abiertos, boca_abierta])

        return caracteristicas

        # detalles_caras = []

        # # print("REKOG LABERS : ",response)
        # if response['FaceDetails']:
        #     print("Se han detectado las siguientes caras:")
        #     for rostro in response['FaceDetails']:
        #         print("Detalles del rostro:")
        #         print("Edad: {}-{}".format(rostro['AgeRange']['Low'], rostro['AgeRange']['High']))
        #         print("Género: {}".format(rostro['Gender']['Value']))
                
        #         # Emoción más prominente
        #         emocion_prominente = max(rostro['Emotions'], key=lambda x: x['Confidence'])
        #         print("Emoción más prominente: {} (Confianza: {})".format(emocion_prominente['Type'], emocion_prominente['Confidence']))
                
        #         # Detalles sobre los atributos faciales
        #         print("Atributos faciales:")
        #         print("- Sonrisa: {} (Confianza: {})".format(rostro['Smile']['Value'], rostro['Smile']['Confidence']))
        #         print("- Uso de gafas: {} (Confianza: {})".format(rostro['Eyeglasses']['Value'], rostro['Eyeglasses']['Confidence']))
        #         print("- Uso de lentes de sol: {} (Confianza: {})".format(rostro['Sunglasses']['Value'], rostro['Sunglasses']['Confidence']))
        #         print("- Presencia de barba: {} (Confianza: {})".format(rostro['Beard']['Value'], rostro['Beard']['Confidence']))
        #         print("- Presencia de bigote: {} (Confianza: {})".format(rostro['Mustache']['Value'], rostro['Mustache']['Confidence']))
        #         print("- Ojos abiertos: {} (Confianza: {})".format(rostro['EyesOpen']['Value'], rostro['EyesOpen']['Confidence']))
        #         print("- Boca abierta: {} (Confianza: {})".format(rostro['MouthOpen']['Value'], rostro['MouthOpen']['Confidence']))
                
        #         print("-------------------------------------------------")
        #         detalle_rostro = {
        #             "edad": "{}-{}".format(rostro['AgeRange']['Low'], rostro['AgeRange']['High']),
        #             "genero": rostro['Gender']['Value'],
        #             "emocion_prominente": max(rostro['Emotions'], key=lambda x: x['Confidence'])['Type'],
        #             "sonrisa": {"valor": rostro['Smile']['Value'], "confianza": rostro['Smile']['Confidence']},
        #             "gafas": {"valor": rostro['Eyeglasses']['Value'], "confianza": rostro['Eyeglasses']['Confidence']},
        #             "lentes_sol": {"valor": rostro['Sunglasses']['Value'], "confianza": rostro['Sunglasses']['Confidence']},
        #             "barba": {"valor": rostro['Beard']['Value'], "confianza": rostro['Beard']['Confidence']},
        #             "bigote": {"valor": rostro['Mustache']['Value'], "confianza": rostro['Mustache']['Confidence']},
        #             "ojos_abiertos": {"valor": rostro['EyesOpen']['Value'], "confianza": rostro['EyesOpen']['Confidence']},
        #             "boca_abierta": {"valor": rostro['MouthOpen']['Value'], "confianza": rostro['MouthOpen']['Confidence']}
        #         }
        #         detalles_caras.append(detalle_rostro)
        # return detalles_caras
    except Exception as e:
        print("Error en la llamada a la API de Rekognition:", e)

def s3_extract_text(image):
    try:
        # Nombre del archivo de la imagen en S3
        nombre_archivo = 'nombre_de_tu_imagen.jpg'

        # Llama a la función detect_text para extraer texto de la imagen
        response = rekognition.detect_text(
            Image={
                'Bytes':image
            }
        )

        # Itera sobre las detecciones de texto en la respuesta
        text = ""
        for text_detection in response['TextDetections']:
            # Imprime el texto detectado
            if text_detection['Type'] == 'WORD':
                text += " " + text_detection['DetectedText']
            # print('Texto detectado:', text_detection['DetectedText'])
        return text
    except Exception as e:
        print("Error en la llamada a la API de Rekognition:", e)