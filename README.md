
# PhraseForge API 
Este proyecto surge de la necesidad de mejorar el vocabulario y la pronunciación del idioma inglés, ya que siempre se recomienda enfocarse en aprender frases completas. De esta idea nació la creación de una API que permite generar estas frases en inglés de manera automatizada.

## ¿Cómo funciona?

![Funcionamiento de API](./readme/api.svg)

Como se aprecia en la imagen, la API se encarga de generar frases en inglés de manera automática apartir de una frase en español. Estas frases se almacenan en una base de datos y se podra acceder en cualquier momento.

## Tabla de Contenidos
1. [Tecnologías](#tecnologías)
2. [Funcionamiento](#funcionamiento)
3. [Uso](#uso)
4. [Endpoints](#endpoints)
5. [Contribuir](#contribuir)
6. [Licencia](#licencia)



# Tecnologías
La API se desarrolló utilizando las siguientes tecnologías:

- PostgreSQL	<img src="./readme/postgresql.svg" alt="PostgreSQL" height="20px" width="20px">

## Python 
<img src="./readme/python.svg" alt="Python" height="40px" width="40px">

La API se desarrolló en Python, utilizando el micro-framework Flask. Utilizando el ORM SQLAlchemy, se crearon las tablas y modelos necesarios para la aplicación. Además, se utilizó Flask-RESTX para crear los endpoints RESTful y Flask-JWT-EXT para gestionar los tokens de autenticación.

## OpenAI
<img src="./readme/openai.svg" alt="OpenAI" height="40px" width="40px">

Se utilizó la API de OpenAI para poder realizar las siguientes tareas:
- Obtener la frase traducida de Español a Inglés.
- Generar con DALL-E un imagen basado en una frase.
- Generar el audio de la frase traducida.

## AWS
<img src="./readme/aws.svg" alt="AWS" height="40px" width="40px" style="display:inline; margin-right:10px;">
<img src="./readme/ubuntu.svg" alt="Ubuntu" height="40px" width="40px" style="display:inline; margin-right:10px;">
<img src="./readme/nginx.svg" alt="Nginx" height="40px" width="40px" style="display:inline; margin-right:10px;">

Para el tema de despliegue, se utilizó el servicio de AWS EC2 utilizando el servidor con el sistema operativo Ubuntu 22.04. Para la creación del servidor web se utilizo Nginx, que se encarga de servir las peticiones HTTP y redireccionarlas a Flask.

## PostgreSQL
<img src="./readme/postgresql.svg" alt="PostgreSQL" height="40px" width="40px">

La base de datos que se utiliza es PostgreSQL. Esto a su vez se encuentra desplegado en un servicio de AWS EC2 con el sistema operativo Ubuntu 22.04.


# Funcionamiento

## Modelado de la base de datos
![Modelado de la base de datos](./readme/backend.svg)