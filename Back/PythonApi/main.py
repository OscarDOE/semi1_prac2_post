
from fastapi import FastAPI, File, UploadFile, Form
import base64


from datetime import datetime
import hashlib
from fastapi.middleware.cors import CORSMiddleware

from db.config import *
from aws.s3 import putobject, deleteobject, getobject, s3_getlink
from aws.rekognition import compare_images, detect_features_in_image, fatial_analisis, s3_extract_text
from models.models import Login, id, Chat
from aws.env import *

app = FastAPI()
# uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acceso desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/register")
async def registeruser(photo: UploadFile = File(...), user: str = Form(...), name: str = Form(...), password: str = Form(...), confpass: str = Form(...)):
    # Confirmar Contraseñas
    if password != confpass:
        return {'Error':'Las contraseñas con coinciden'}
    # Confirmar si ya existe el usuario
    exists_sql = f"SELECT EXISTS (SELECT 1 FROM user WHERE user = %s) AS user_exists"
    params = (user,)
    response = execute_query(exists_sql, params)
    # print("RESPONSE", response)
    print("ANTEs DE IF: ",response)
    if response[0] == 1:
        return {'Error':'El nombre de usuario ya existe '}
    if response == False :
        return {"Error":"Usuario no insertado, problemas con el usuario"}

    # Subir a S3
    file_contents = await photo.read()
    actual_date = datetime.now()
    key = 'Fotos_Perfil/'+user+";"+photo.filename.split(".")[0]+str(actual_date)+".jpg"
    user = key.split(";")[0].split("/")[-1]
    print("ENCONTRO EL USER",user)

    passwordcode = hashlib.md5(password.encode()).hexdigest()

    # Aquí puedes procesar el archivo (file_contents) o guardarlos en S3, etc.
    putobject(key, file_contents)
    insert_sql = f"INSERT INTO user (user, name, password, photo) VALUES (%s, %s, %s, %s)"
    params = (user, name, passwordcode, key)
    response = execute_query(insert_sql, params)

    print("RESPONSE", response)
    
    if response == False :
        return {"Error":"Usuario no insertado"}

    last_id = response[1]
        

    insert_sql_photo = f"INSERT INTO photoprofile (name, photo, user_id) VALUES (%s, %s, %s)"
    params = (name, key, last_id)
    response = execute_query(insert_sql_photo, params)
    if response:
        return {"mensaje":"Usuario insertado con éxito"}
    else:
        return {"Error":"No se agregó imágen "}


@app.post("/login")
async def loginuser(item: Login):
    sql = f"SELECT COUNT(*) AS exist FROM user WHERE user = %s AND password = %s"
    passwordcode = hashlib.md5(item.password.encode()).hexdigest()
    params = (item.user, passwordcode)
    response = execute_query(sql, params)
    print(response)
    print("RERERE",response[0])
    if response[0][0] == 0:
        return {"Error": "El usuario o la contraseña no coinciden"}
    sql = f"SELECT user, name, photo, id FROM user WHERE user = %s"
    params = (item.user,)
    response = execute_query(sql, params)
    
    link = s3_getlink(response[0][2])

    print("KEY",response[0][2])
    features = fatial_analisis(response[0][2])
    features = features['FaceDetails'][0]
    print(features)



    # print("RESPONSE LOGIN", response[0])
    toreturn = {"user":response[0][0],
            "name":response[0][1],
            "photo":link,
            "id":response[0][3],
            "features":features
    }
    return toreturn
    # return {"mensaje": "Contraseña confirmada",
    #         "user" : item.user}

@app.post("/camera_login")
async def login_camera(photo: UploadFile = File(...), user: str = Form(...)):
    sql = f"SELECT COUNT(*) AS exist FROM user WHERE user = %s"
    params = (user)
    response = execute_query(sql, params)

    print(response)
    print("RERERE",response[0])
    if response[0][0] == 0:
        return {"Error": "El usuario o la contraseña no coinciden"}
    sql = f"SELECT user, name, photo, id FROM user WHERE user = %s"
    params = (user,)
    response = execute_query(sql, params)
    

    file_contents = await photo.read()
    profile_photo = response[0][2]
    compare = compare_images(profile_photo, file_contents)

    link = s3_getlink(response[0][2])
    features = fatial_analisis(response[0][2])
    features = features['FaceDetails'][0]


    toreturn = {"user":response[0][0],
            "name":response[0][1],
            "photo":link,
            "id":response[0][3],
            "features":features,
    }
    return toreturn



@app.post("/editprofile")
async def edituserprofile(photo: UploadFile = File(None), name: str = Form(...), password: str = Form(...), newuser: str = Form(...), id: int = Form(...)):
    print("ENTRE", photo )
    sql = f"SELECT COUNT(*) AS exist FROM user WHERE id = %s AND password = %s"
    print("PASS", password )
    print("USER", id )
    passwordcode = hashlib.md5(password.encode()).hexdigest()
    print("PASSCODE", passwordcode )
    params = (id, passwordcode)
    response = execute_query(sql, params)

    if response[0] == 0:
        return {"Error": "El usuario o la contraseña no coinciden"},400

    sql = ""
    params = ()
    lastuser = ""
    insert_sql_photo =""
    params_phot = ()
    link = ""
    if photo == None:
        print("ENTRE NO PHOT", photo )
        sql = f"UPDATE user SET user=%S, name = %s FROM user WHERE id = %s"
        params = (newuser, name, id)
    else:
        print("ENTRE SI HOTO", photo )
        # Subir a S3
        file_contents = await photo.read()
        actual_date = datetime.now()
        key = 'Fotos_Perfil/'+str(id)+";"+photo.filename+str(actual_date)
        user = key.split(";")[0].split("/")[-1]
        link = putobject(key, file_contents)
        
        insert_sql_photo = f"INSERT INTO photoprofile (name, photo, user_id) VALUES (%s, %s, %s)"
        params_phot = (name, link, id)
        response = execute_query(insert_sql_photo, params_phot)
        sql = f"UPDATE user SET user=%s, name = %s , photo = %s WHERE id = %s"
        params = (newuser, name, link, id)

    response = execute_query(sql, params)
    print("FINAL", photo )
    if response :
        toreturn = {"user":newuser,
            "name":name,
            "photo":link,
            "id":id
        }
        return toreturn
    else:
        return {"Error":"No se ha podido editar al usuario"},400


# @app.post("/createalbum")
# async def editalbum(item: Createalbum):
#     insert_sql = f"INSERT INTO album (user_id, name) VALUES (%s, %s)"
#     params = (item.id, item.album)
#     response = execute_query(insert_sql, params)
#     print(response)
#     if response :
#         return {"mensaje":"Álbum creado correctamente"}
#     else:
#         return {"Error":"No se ha podido crear el álbum"}

@app.post("/justalbums")
async def seealbum(item: id):
    sql = f"SELECT * FROM album WHERE user_id= %s"
    sss = str(item.user)
    params = (sss,)
    response = execute_query(sql, params)
    print(response)
    albumes = []
    for dato in response:
        albumes.append({"title": dato[1].capitalize(), "id": dato[0]})
    print(albumes)
    return albumes

# @app.post("/editalbum")
# async def editalbum(item: Editalbum):
#     sql = f"UPDATE album SET name = %s WHERE id = %s AND user_id = %s"
#     params = (item.newalbum, item.id_album, item.id)
#     response = execute_query(sql, params)
#     if response :
#         return {"mensaje":"Álbum editado correctamente"}
#     else:
#         return {"Error":"No se ha podido editar al álbum"}

# @app.post("/deletealbum")
# async def deletealbum(item: id):
#     entero = int(item.user)
#     sql = f"DELETE FROM album WHERE id = %s"
#     params = (item.user,)
#     response = execute_query(sql, params)
#     print(item)
#     if response :
#         return {"mensaje":"Álbum eliminado correctamente"}
#     else:
#         return {"Error":"No se ha podido eliminar al álbum"}


@app.post("/upload")
async def uploadimage(photo: UploadFile = File(...), name: str = Form(...), id: str = Form(...), description: str = Form(...)):
    # OBtener Imagen y llave
    file_contents = await photo.read()
    actual_date = datetime.now()
    key = 'Fotos_Publicadas/'+id+";"+photo.filename.split(".")[0]+str(actual_date)
    user = key.split(";")[0].split("/")[-1]
    print("ENCONTRO EL USER",user)

    # Verificar si se creará un nuevo album
    isnewalbum = detect_features_in_image(file_contents)
    print("ENCONTRO EL USER",isnewalbum[0])
    print("************************** SALIO")

    exists_sql = f"SELECT EXISTS (SELECT 1 FROM album WHERE name = %s AND user_id = %s) AS user_exists"
    params = (isnewalbum[0], id)
    response = execute_query(exists_sql, params)
    # print("RESPONSE", response)
    print("ANTEs DEL CREAR ALBUM:  ",response)
    if response and response[0][0] == 1:
        print("Ya existe")
    else:
        print("ENTRO  A NUEVO ALBUM:  ")
        # El nombre de album ya existe para este usuario
        insert_sql = f"INSERT INTO album (user_id, name) VALUES (%s, %s)"
        params = (id, isnewalbum[0])
        response = execute_query(insert_sql, params)
        print(response)

    # Agregando a S3
    putobject(key, file_contents)
    # Ingresando a album la imagen, confirmando que existe solo 1
    last_id_sql = f"SELECT id FROM album WHERE name = %s AND user_id = %s"
    params = (isnewalbum[0], id)
    response = execute_query(last_id_sql, params)
    if(len(response) > 1):
        return {"Error": "Hay más de 1 album con ese nombre"}
    print("LAST ID:  ",response, " SOLO ID: ", response[0][0])
    last_id = response[0][0]
    # Insertando la foto
    insert_sql = f"INSERT INTO photoalbum (photo, album_id, name, description ) VALUES (%s, %s, %s, %s)"
    params = (key, last_id, name, description)

    response = execute_query(insert_sql, params)
    if response :
        return {"mensaje":"Foto subida correctamente"}
    else:
        return {"Error":"No se ha podido subir la foto"}


@app.post("/albums")
async def seealbum(item: id):
    sql = f"SELECT a.id AS ID_ALBUM, pa.photo AS photo_album, a.name AS album_name, pa.name AS photo_name, pa.id AS ID_PHOTO FROM user u JOIN album a ON u.id = a.user_id JOIN photoalbum pa ON a.id = pa.album_id WHERE u.id = %s"
    params = (item.user,)
    response = execute_query(sql, params)
    print("RESPONSE 1: ",response)

    albums = {}
    for album_id, photo_album, album_name, photo_name, photo_id in response:
        # Si el álbum ya está en el diccionario, agregamos la imagen al álbum existente
        if album_id in albums:
            albums[album_id]["fotos"].append({"id": photo_id, "url": photo_album, "descripcion": photo_name})
        # Si no, creamos un nuevo álbum y agregamos la imagen al álbum
        else:
            albums[album_id] = {"id": album_id, "nombre": album_name, "fotos": [{"id": photo_id, "url": photo_album, "descripcion": photo_name}]}

    formatted_data = list(albums.values())

    sql = f"SELECT pp.photo AS photo_profile, pp.name AS photo_name FROM user u JOIN photoprofile pp ON u.id = pp.user_id WHERE u.id = %s"
    response2 = execute_query(sql, params)
    print("-------------------- ")
    print("RESPONSE2, ",response2)

    formatted_data2 = [{"url": item[0], "usuario": item[1]} for item in response2]
    # formatted_data.append(formatted_data2)
    arreglo = [formatted_data]
    arreglo.append(formatted_data2)
    return arreglo

@app.post("/albumsprofile")
async def seealbum(item: id):
    sql = f"SELECT pp.photo AS photo_profile, pp.name AS photo_name FROM user u JOIN photoprofile pp ON u.id = pp.user_id WHERE u.id = %s"
    params = (item.user,)
    response = execute_query(sql, params)
    print(response)
    album = ""
    for i in response[0]:
        print("I",i)
    toreturn = {"user":response[0],
            "name":response[1],
            "photo":response[2]
    }
    return toreturn

@app.post("/extracttext")
async def extractingtext(photo: UploadFile = File(...)):
    file_contents = await photo.read()
    response = s3_extract_text(file_contents)
    print(response)

    
    return response
@app.post("/send_2bot")
async def chatbot(item: Chat):
    
    return True

# @app.get("/")
# def get_main():
#     cursor = cnx.cursor()
#     query = "SELECT * FROM games"
#     cursor.execute(query)
#     users = cursor.fetchall()
#     cursor.close()
#     print("juegos",users)
#     return {"juegos":users}


# @app.get("/users")
# def get_users():
#     cursor = cnx.cursor()
#     query = "SELECT * FROM users"
#     cursor.execute(query)
#     users = cursor.fetchall()
#     cursor.close()
#     return {"users": users}

# @app.get("/dbtest")
# def test_db_connection():
#     cursor = cnx.cursor()
#     cursor.execute("SELECT VERSION()")
#     result = cursor.fetchone()
#     cursor.close()
#     return {"db_version": result[0]}

