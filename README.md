# Ponderara---Login-CRUD-Postegre
# Atividade 2: Criação de uma aplicação protegida com CRUD

Esta atividade tem por objetivo desenvolver um projeto web que possibilite os usuários registrarem dados em um banco de dados. O deploy do banco, da API do backend e do frontend deve acontecer utilizando uma aplicação com multiplos containers. A aplicação não precisa utilizar frameworks, pode ser realizada utilizando os primitivos presentes na linguagem de programação escolhida.

## Rodando a aplicação

Para rodar a aplicação, primeiramente devemos puxar a aplicação que está em um repositório no Docker Hub.
O container que será puxado é do seguinte perfil:

`kilmatheus/podenrada-crud`

Para executar a aplicação, siga os seguintes passos:

1. Faça o Download da aplicação do Docker Desktop: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Inicie a aplicação e faça o cadastro até a tela inicial da aplicação.

3. Com a aplicação rodando, abra o terminal e execute o seguinte comando para puxar a imagem:

```bash
docker pull kilmatheus/ponderada-crude:2.0.0
```

4. Após puxar, execute o seguinte comando para rodar o contêiner:

```bash
docker run -p 8000:8000 kilmatheus/curriculo-ponderada1:1.0.0
```

Assim, a aplicação vai rodar e será possível acessar no navegador.

Caso queira rodar a sua própria aplicação seguindo um processo semelhante, siga estas etapas:

Executando sua própria aplicação containerizada
Aqui estão os passos para executar sua própria aplicação usando Docker:

1. Construindo a Imagem Docker
Certifique-se de que você possui um Dockerfile no diretório da sua aplicação. O Dockerfile define como a imagem do contêiner deve ser construída. Aqui está um exemplo, no meu caso, no diretório Flask:

```bash
# Imagem Base: python:3.9
FROM python:3.9-alpine

# Diretorio dentro da imagem que vamos trabalhar
WORKDIR /code

# Copia o arquivo requirements.txt para dentro da imagem
COPY ./requirements.txt /code/requirements.txt

# Instala as dependencias do projeto
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o conteudo do diretorio atual para dentro da imagem
COPY . /code

# Expoe a porta 80
EXPOSE 80

# Executa o comando python main.p
CMD ["python", "main.py"]
```

2. E depois no meu diretório db:

```bash
# Use uma imagem do PostgreSQL
FROM postgres:latest

# Defina as variáveis de ambiente do PostgreSQL
ENV POSTGRES_DB = postgres
ENV POSTGRES_USER = postgres
ENV POSTGRES_PASSWORD = senha

# Copie o arquivo SQL com os comandos para criar as tabelas
COPY init.sql /docker-entrypoint-initdb.d/
```

3. E na pasta Raiz o meu Docker Compose, para compilar as duas imagens.

```bash
version: '3.1'

services:

  db:
    build:
      context: ./db
      dockerfile: Dockerfile
    restart: always
    environment:
      POSTGRES_PASSWORD: senha
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
    ports:
      - 5432:5432
    container_name: meu-db
    
  adminer:
    image: adminer
    restart: always
    ports:
      - 8080:8080
    depends_on:
      - db
    container_name: adminer

  app:
    build: ./flask
    restart: always
    ports:
      - 8000:8000
    depends_on:
      - db
    container_name: meu-app
```

Sendo assim, foi construido essa aplicação.