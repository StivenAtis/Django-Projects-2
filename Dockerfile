# Pull base image
FROM python:3.10.4-slim-bullseye
# Set environment variables
# Desactiva la verificación de versiones de pip para evitar advertencias durante las instalaciones.
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# Evita la creación de archivos ".pyc" (código compilado de Python) para mantener limpio el sistema de archivos.
ENV PYTHONDONTWRITEBYTECODE 1
# Evita que Python almacene archivos de caché en el sistema de archivos.
ENV PYTHONUNBUFFERED 1
# Set work directory
# Establece el directorio de trabajo en el contenedor.
WORKDIR /Django-projects-2
# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Copy project
COPY . .