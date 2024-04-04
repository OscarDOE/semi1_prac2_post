# Manual de configuracion - Practica 2 - Seminario de Sistemas 1

| Nombre                           | Carné    |
|----------------------------------|----------|
| Juan Sebastian Julajuj Zelada    | 201905711|
| Carlos Estuardo Monterroso Santos| 201903767|
| Oscar Daniel Oliva España        | 201902663|


## Descripción de la arquitectura AWS
Implementación básica de un sistema web que utiliza una variedad de servicios de AWS. A continuación se describe cada componente de la arquitectura y los servicios de AWS que se utilizan:

Componentes de la arquitectura:

* App Web: La aplicación web es la interfaz de usuario del sistema. Puede ser una aplicación web desarrollada en Python, NodeJS o cualquier otro lenguaje de programación web.
* Servidor Publico: El servidor publico de la aplicación web puede ser un servidor EC2.
* Bucket de Imágenes: El bucket de imágenes se utiliza para almacenar las imágenes que se utilizan en la aplicación web. Se puede usar Amazon S3 para este propósito.
* Base de Datos: La base de datos almacena los datos del sistema. Puede ser una base de datos relacional como Amazon RDS.
* Motor de chatbot: El motor de chatbot se encarga de la interacción con los usuarios a través de un chatbot. Puede ser un servicio como Amazon Lex.
* Análisis de Imágenes: El análisis de imágenes se utiliza para procesar y analizar las imágenes que se suben al sistema. Puede ser un servicio como Amazon Rekognition.

Servicios de AWS utilizados:

* Amazon EC2: Se utiliza para crear y ejecutar servidores en la nube.
* Amazon S3: Se utiliza para almacenar archivos en la nube.
* Amazon RDS: Se utiliza para crear y ejecutar bases de datos relacionales en la nube.
* Amazon Lex: Se utiliza para crear chatbots.
* Amazon Rekognition: Se utiliza para analizar imágenes.

Flujo de trabajo:

Un usuario interactúa con la aplicación web.

La aplicación web interactúa con el servidor publico.

El servidor publico interactúa con el bucket de imágenes para recuperar las imágenes que se muestran en la aplicación web.

La aplicación web interactúa con la base de datos para obtener los datos que se muestran en la aplicación web.

La aplicación web interactúa con el motor de chatbot para procesar la interacción con el usuario.

El motor de chatbot puede interactuar con Amazon Lex para generar respuestas a los usuarios.

La aplicación web puede interactuar con Amazon Rekognition para analizar imágenes que se suben al sistema.


## Descripción de los diferentes usuarios de IAM

* Usuarios IAM para RDS (Amazon Relational Database Service):

Estos usuarios IAM deben tener permisos para crear, modificar o eliminar instancias de bases de datos, realizar copias de seguridad, restaurar instantáneas, entre otros.
Es fundamental aplicar el principio de privilegio mínimo, es decir, otorgar solo los permisos necesarios para realizar las tareas requeridas y evitar la asignación de permisos excesivos.

* Usuarios IAM para Lex:

Estos usuarios necesitan permisos para crear, modificar y eliminar bots, así como para acceder a otros recursos asociados, como alias, versiones y logs.
Los permisos también pueden incluir la capacidad de interactuar con otros servicios de AWS, como Lambda (para integraciones de funciones) o S3 (para almacenar recursos de bot, como archivos de audio o imágenes).

* Usuarios IAM para Rekognition:

Los usuarios IAM para Rekognition necesitan permisos para utilizar las funciones ofrecidas por el servicio, como analizar imágenes, crear colecciones de rostros, realizar comparaciones de caras, etc.
Los usuarios pueden necesitar acceso a otros recursos de AWS, como S3 para almacenar imágenes o DynamoDB para almacenar metadatos relacionados con el análisis de imágenes.

* Usuarios IAM para Translate:

Los usuarios IAM para Translate se utilizan para interactuar con el servicio y realizar traducciones de texto.
Estos usuarios necesitan permisos para utilizar las funciones de traducción ofrecidas por el servicio, así como acceso a los recursos de AWS necesarios para almacenar y gestionar los textos a traducir, como S3 para almacenar archivos de texto.


## Funciones de Amazon Rekognition

* Detect Labels

Detecta y devuelve etiquetas de objetos y escenas en una imagen.

Útil para identificar objetos y escenas presentes en imágenes.

Aplicaciones como clasificación de imágenes, etiquetado automático, análisis de contenido visual.

* Compare Faces

Compara las caras en dos imágenes y determina si pertenecen a la misma persona.

Util para la verificación de identidad, reconocimiento facial y análisis de similitud entre caras.

Aplicaciones como autenticación biométrica, seguridad, detección de fraudes.

* Extract Text

Extrae texto de imágenes, incluidos documentos y carteles.

Util para convertir texto en imágenes en texto digital para su procesamiento adicional.

Aplicaciones como reconocimiento óptico de caracteres (OCR), digitalización de documentos, búsqueda de texto en imágenes.

* Face Analysis

Analiza las caras en una imagen para obtener información detallada, como edad, género, emociones y más.

Util para comprender las características faciales y emocionales de las personas en imágenes.

Aplicaciones como análisis de audiencia, segmentación de mercado, personalización de contenido, investigación psicológica.


## Funcionalidades para un Chat Bot

* "Alquilar" una casa como Airbnb

:house_with_garden: Busca y reserva alojamiento temporal en una casa o apartamento similar a Airbnb.

Ideal para encontrar y alquilar propiedades para estancias cortas o vacaciones.

Planificación de viajes, reservas de alojamiento, turismo.

* Comprar una laptop

:computer: Explora y adquiere una computadora portátil según tus necesidades y preferencias.

Para encontrar y comprar laptops de diferentes marcas y especificaciones técnicas.

Compras en línea, comparación de productos, tecnología.

* Comprar un teléfono

:iphone: Encuentra y adquiere un teléfono móvil que se ajuste a tus requerimientos y presupuesto.

Para buscar y comprar teléfonos inteligentes de diversas marcas y modelos.

Compras en línea, comparación de dispositivos, comunicación móvil.

