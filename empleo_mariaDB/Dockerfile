# Imagen base
FROM mariadb:latest

# Variables de entorno
ENV MARIADB_ROOT_PASSWORD=admin
ENV MARIADB_DATABASE=empleosDBmariaDB

# Copiar script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer puerto
EXPOSE 3306
