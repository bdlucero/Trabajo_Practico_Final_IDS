SkillMatch UBA 

Plataforma web para buscar y compartir materiales académicos de FIUBA: apuntes, parciales, finales, enlaces, repositorios e imágenes, filtrados por materia, tipo y formato. 

Trabajo Práctico Final – Ingeniería de Software (IDS) – FIUBA. 

Tecnologías utilizadas: 

- Python 3 

- Flask (Frontend y Backend) 

- MySQL 

- HTML, CSS, JavaScript 

- python-dotenv 

- flask-cors 

- requests 

- mysql-connector-python 

- PythonAnywhere (hosting) 

Requisitos previos 

- Python 3 

- Git 

- MySQL Server instalado 

- Linux/WSL recomendado 

Instalación del entorno (local) 

1. Clonar el repositorio 

git clone https://github.com/bdlucero/Trabajo_Practico_Final_IDS 

cd Trabajo_Practico_Final_IDS 

2. Crear entorno virtual e instalar dependencias 

chmod +x init.sh 

./init.sh 

3. Activar entorno virtual 

source venv/bin/activate 

Configuración de variables de entorno 

El proyecto incluye un archivo .env.example en FrontEnd,  los datos de ese archivo
deben ser reemplazado por el .env real para su funcionamiento. El archivo .env real NO se sube al repositorio 

CONFIGURACION ADICIONALES EN FRONTEND
Desde la raíz del proyecto:
cd FrontEnd
cp .env.example .env
Contenido: 
SECRET_KEY= aqui va la clave privada 
BACKEND_URL=http://127.0.0.1:5050/ (SE DEJA IGUAL)
GOOGLE_CLIENT_ID= aqui va el cliente de id privado

Luego editar el archivo .env y reemplazar los valores de ejemplo por los reales

BASE DE DATOS
Crear base: 
CREATE DATABASE skillmatch_uba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Importar script: 
mysql -u tu_usuario -p skillmatch_uba < skillmatch_uba.sql 
(El archivo skillmatch_uba.sql contiene el esquema
y los datos iniciales necesarios para probar la aplicación.)

EJECUCION LOCAL
para el backend:
cd BackEnd 
python app.py 
Disponible en http://127.0.0.1:5050/ 

para el Frontend: 
cd FrontEnd 
python app.py 
Disponible en http://127.0.0.1:5000/ 

HOSTING EN PYTHON ANYWHERE
El proyecto puede visualizarse online: 
https://alejandroxr10.pythonanywhere.com/ 
