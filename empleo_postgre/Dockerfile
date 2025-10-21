# Imagen base PostgreSQL
FROM postgres:latest

# Variables de entorno
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=empleosDB

# Copiar script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer puerto PostgreSQL
EXPOSE 5432
