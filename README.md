# Mapa de áreas de Jacareí

## Requisitos

- Python 3.10 ou superior
- PostgreSQL em execução

## Configuração

1. Crie o banco `areas_db` no PostgreSQL.
2. Execute `src/banco/schema.sql` conectado ao banco `areas_db`.
3. Configure `DATABASE_URL` com os dados da sua conexão. No PowerShell:

   ```powershell
   $env:DATABASE_URL = "postgresql://postgres:SUA_SENHA@localhost:5432/areas_db"
   ```

4. Instale as dependências e inicie o Flask na raiz do projeto:

   ```powershell
   py -m pip install -r requirements.txt
   py -m src.back.app
   ```

5. Acesse http://127.0.0.1:5000.

## Como funciona

Cada área é um polígono desenhado no mapa, cadastrado com nome e **um ou mais tipo**
(escolar, industrial, residencial). Não existe mais cadastro de pontos: o tipo é
informado diretamente no polígono. Uma área pode ter dois tipo (ex.: escolar e
industrial) e polígonos podem se sobrepor; ao clicar no mapa, o sistema devolve a
união dos tipo de todos os polígonos que contêm o ponto.

`src/banco/seed.sql` contém dados fictícios opcionais para teste.

### Já tenho o banco antigo (com a tabela `pontos`)

Execute uma vez `src/banco/migracao_remove_pontos.sql`. Ele adiciona a coluna `tipo`
em `areas` (as áreas existentes ficam como residencial até você ajustar) e apaga `pontos`.

### Testes

```powershell
py -m unittest src.back.test_geometria src.back.test_app
```
