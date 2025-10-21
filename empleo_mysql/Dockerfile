# Imagen base
FROM mysql:latest

# Variables de entorno
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=empleosDBmysql

# Copiar script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer puerto MySQL
EXPOSE 3306
