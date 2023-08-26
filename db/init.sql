CREATE TABLE usuario (
    username TEXT PRIMARY KEY,
    senha TEXT NOT NULL
);

CREATE TABLE bloco (
    title TEXT PRIMARY KEY,
    contents TEXT
);

INSERT INTO bloco VALUES ('Teste', 'Valor criar direto do init.sql');