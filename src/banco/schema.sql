-- TODO: Tabela areas -> recebe id, nome, tipo (industrial, escolar ou residencial) e coordenadas (fazer com JSONB por ser resposta de API)

CREATE TABLE IF NOT EXISTS areas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo TEXT NOT NULL
        CHECK (tipo IN ('escolar', 'industrial', 'residencial')), -- regra de validação! 
    coordenadas JSONB NOT NULL
);
