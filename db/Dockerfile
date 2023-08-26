# Use uma imagem do PostgreSQL
FROM postgres:latest

# Defina as variáveis de ambiente do PostgreSQL
ENV POSTGRES_DB = postgres
ENV POSTGRES_USER = postgres
ENV POSTGRES_PASSWORD = senha

# Copie o arquivo SQL com os comandos para criar as tabelas
COPY init.sql /docker-entrypoint-initdb.d/