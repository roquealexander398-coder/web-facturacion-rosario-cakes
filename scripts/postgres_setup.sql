-- Script de configuración inicial de PostgreSQL

-- Crear usuario de base de datos
CREATE USER facturacion_user WITH PASSWORD 'secure_password_123';

-- Crear base de datos
CREATE DATABASE facturacion_db 
    OWNER facturacion_user
    ENCODING 'UTF8'
    LC_COLLATE 'Spanish_Dominican Republic.1252'
    LC_CTYPE 'Spanish_Dominican Republic.1252'
    TEMPLATE template0;

-- Conceder privilegios
GRANT ALL PRIVILEGES ON DATABASE facturacion_db TO facturacion_user;

-- Configuración de conexión
ALTER DATABASE facturacion_db SET client_encoding TO 'UTF8';
ALTER DATABASE facturacion_db SET default_transaction_isolation TO 'read committed';
ALTER DATABASE facturacion_db SET timezone TO 'America/Santo_Domingo';

-- Crear extensión para UUID (opcional)
\c facturacion_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verificar configuración
SELECT datname, datcollate, datctype 
FROM pg_database 
WHERE datname = 'facturacion_db';

-- Mostrar usuarios
SELECT usename FROM pg_user;

-- Mostrar bases de datos
SELECT datname FROM pg_database;