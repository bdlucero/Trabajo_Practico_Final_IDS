#!/usr/bin/env bash 

set -e 

 if ! command -v python3 >/dev/null 2>&1; then 

    echo "Error: python3 no está instalado." 

    exit 1 

fi 

 python3 -m venv venv 

source venv/bin/activate 

pip install --upgrade pip 

pip install -r FrontEnd/requirementsback.txt

pip install -r BackEnd/requirementsfront.txt

echo "Entorno listo. Ejecutá: source venv/bin/activate" 
