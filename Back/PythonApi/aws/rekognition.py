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
        # print("RESPONSE FATIAL: ", response)
        return response
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