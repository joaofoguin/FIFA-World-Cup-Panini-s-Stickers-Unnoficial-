# API de Figurinhas da Copa

API desenvolvida em **FastAPI** para gerenciamento do catálogo de figurinhas do aplicativo **Álbum da Copa**.

A API é responsável por armazenar e disponibilizar o catálogo oficial de figurinhas, contendo informações como número no álbum, nome, país e ordem do país no álbum. A coleção pessoal do usuário é salva localmente no aplicativo Flutter, evitando armazenamento de dados pessoais no servidor.

---

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Supabase
- Vercel
- Uvicorn
- Pydantic

---

## Objetivo da API

Esta API tem como objetivo centralizar o catálogo oficial de figurinhas da Copa.

Ela permite:

- cadastrar figurinhas;
- listar todas as figurinhas;
- buscar figurinha por ID;
- buscar figurinha pelo número/código do álbum;
- listar figurinhas por país;
- atualizar dados de uma figurinha;
- remover figurinhas;
- cadastrar várias figurinhas em lote.

A API **não armazena a coleção pessoal do usuário**. Informações como figurinhas possuídas, repetidas e faltantes são salvas localmente no aplicativo Flutter.

---

## Arquitetura do projeto

```text
Flutter App
   ↓
API FastAPI publicada na Vercel
   ↓
Banco PostgreSQL no Supabase
````

A API armazena apenas dados públicos do catálogo:

```text
id
numero_album
nome
pais
ordem_pais
```

O aplicativo Flutter salva localmente:

```text
numero_album
quantidade
```

Dessa forma, o servidor sabe quais figurinhas existem, mas não sabe quais figurinhas cada usuário possui.

---

## Estrutura de pastas

```text
api-figurinhas-copa/
│
├── api/
│   ├── __init__.py
│   ├── index.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

---

## Modelo de dados

### Figurinha

| Campo          | Tipo    | Descrição                                |
| -------------- | ------- | ---------------------------------------- |
| `id`           | Integer | Identificador interno da figurinha       |
| `numero_album` | String  | Código/número da figurinha no álbum      |
| `nome`         | String  | Nome do jogador, brasão ou item especial |
| `pais`         | String  | País ou seleção da figurinha             |
| `ordem_pais`   | Integer | Ordem do país no álbum                   |

Exemplo:

```json
{
  "id": 1,
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

O campo `numero_album` é do tipo `String` porque alguns códigos podem ser alfanuméricos, como:

```text
MEX1
RSA10
BRA5
ARG12
```

---

## Instalação local

Clone o repositório:

```bash
git clone https://github.com/joaofoguin/album-checklist-api
```

Entre na pasta do projeto:

```bash
cd api-figurinhas-copa
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sua_url_do_postgresql
```

Exemplo de formato:

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/postgres
```

Para deploy na Vercel com Supabase, recomenda-se usar a URL do **Transaction Pooler** do Supabase.

Exemplo de formato:

```env
DATABASE_URL=postgresql://postgres.PROJECT_REF:SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

O arquivo `.env` não deve ser enviado para o GitHub.

---

## Rodando localmente

Execute:

```bash
uvicorn api.index:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação Swagger estará disponível em:

```text
http://127.0.0.1:8000/docs
```

---

## Deploy na Vercel

O projeto já contém o arquivo `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

Para publicar:

1. Envie o projeto para o GitHub.
2. Importe o repositório na Vercel.
3. Configure a variável de ambiente `DATABASE_URL`.
4. Faça o deploy.

Após o deploy, a API ficará disponível em uma URL parecida com:

```text
https://api-figurinhas-copa.vercel.app
```

---

## Endpoints

### Verificar status da API

```http
GET /
```

Resposta:

```json
{
  "mensagem": "API de Figurinhas da Copa está online!"
}
```

---

### Cadastrar uma figurinha

```http
POST /figurinhas
```

Corpo da requisição:

```json
{
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

Resposta:

```json
{
  "id": 1,
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

---

### Cadastrar figurinhas em lote

```http
POST /figurinhas/lote
```

Corpo da requisição:

```json
[
  {
    "numero_album": "RSA1",
    "nome": "BRASÃO",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  },
  {
    "numero_album": "RSA2",
    "nome": "RONWEN WILLIAMS",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  },
  {
    "numero_album": "RSA3",
    "nome": "SIPHO CHAINE",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  }
]
```

Observação: para cadastro em lote, o corpo precisa ser uma lista JSON, ou seja, deve começar com `[` e terminar com `]`.

---

### Listar todas as figurinhas

```http
GET /figurinhas
```

Resposta:

```json
[
  {
    "id": 1,
    "numero_album": "RSA1",
    "nome": "BRASÃO",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  },
  {
    "id": 2,
    "numero_album": "RSA2",
    "nome": "RONWEN WILLIAMS",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  }
]
```

A listagem é ordenada por:

```text
ordem_pais
numero_album
```

---

### Buscar figurinha por ID

```http
GET /figurinhas/{figurinha_id}
```

Exemplo:

```http
GET /figurinhas/1
```

Resposta:

```json
{
  "id": 1,
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

---

### Buscar figurinha pelo número/código do álbum

```http
GET /figurinhas/numero/{numero_album}
```

Exemplo:

```http
GET /figurinhas/numero/RSA1
```

Resposta:

```json
{
  "id": 1,
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

---

### Listar figurinhas por país

```http
GET /figurinhas/pais/{pais}
```

Exemplo:

```http
GET /figurinhas/pais/ÁFRICA DO SUL
```

Resposta:

```json
[
  {
    "id": 1,
    "numero_album": "RSA1",
    "nome": "BRASÃO",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  },
  {
    "id": 2,
    "numero_album": "RSA2",
    "nome": "RONWEN WILLIAMS",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  }
]
```

---

### Atualizar figurinha

```http
PUT /figurinhas/{figurinha_id}
```

Exemplo:

```http
PUT /figurinhas/1
```

Corpo da requisição:

```json
{
  "numero_album": "RSA1",
  "nome": "BRASÃO OFICIAL",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

Resposta:

```json
{
  "id": 1,
  "numero_album": "RSA1",
  "nome": "BRASÃO OFICIAL",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

---

### Remover figurinha

```http
DELETE /figurinhas/{figurinha_id}
```

Exemplo:

```http
DELETE /figurinhas/1
```

Resposta:

```json
{
  "mensagem": "Figurinha removida com sucesso."
}
```

---

## Códigos de erro comuns

### 400 - Figurinha já cadastrada

Ocorre quando já existe uma figurinha com o mesmo `numero_album`.

Exemplo:

```json
{
  "detail": "Já existe uma figurinha com esse número no álbum."
}
```

---

### 404 - Figurinha não encontrada

Ocorre quando o ID ou número informado não existe.

Exemplo:

```json
{
  "detail": "Figurinha não encontrada."
}
```

---

### 422 - Erro de validação

Ocorre quando o corpo da requisição não está no formato esperado.

Exemplo comum: tentar enviar várias figurinhas no endpoint que aceita apenas uma.

Errado em `POST /figurinhas`:

```json
{
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
},
{
  "numero_album": "RSA2",
  "nome": "RONWEN WILLIAMS",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

Correto para uma figurinha:

```json
{
  "numero_album": "RSA1",
  "nome": "BRASÃO",
  "pais": "ÁFRICA DO SUL",
  "ordem_pais": 3
}
```

Correto para várias figurinhas em lote:

```json
[
  {
    "numero_album": "RSA1",
    "nome": "BRASÃO",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  },
  {
    "numero_album": "RSA2",
    "nome": "RONWEN WILLIAMS",
    "pais": "ÁFRICA DO SUL",
    "ordem_pais": 3
  }
]
```

---

## Banco de dados

A tabela principal é `figurinhas`.

Exemplo de estrutura SQL:

```sql
CREATE TABLE figurinhas (
    id SERIAL PRIMARY KEY,
    numero_album VARCHAR UNIQUE NOT NULL,
    nome VARCHAR NOT NULL,
    pais VARCHAR NOT NULL,
    ordem_pais INTEGER NOT NULL
);
```

---

## Privacidade

A API armazena somente o catálogo oficial de figurinhas.

Ela não armazena:

* nome do usuário;
* e-mail;
* login;
* coleção pessoal;
* figurinhas possuídas;
* figurinhas repetidas;
* histórico individual.

A coleção do usuário é salva localmente no aplicativo Flutter, reduzindo a exposição de dados pessoais e simplificando a arquitetura inicial do projeto.

---

## Integração com o aplicativo Flutter

O aplicativo Flutter consome a API para obter o catálogo oficial das figurinhas.

Exemplo de endpoint consumido:

```http
GET /figurinhas
```

O aplicativo salva localmente apenas:

```text
numero_album
quantidade
```

Com essa lógica:

```text
quantidade = 0 → figurinha faltante
quantidade = 1 → figurinha possuída
quantidade > 1 → figurinha possuída + repetidas
```

---

## Exemplo de fluxo no app

1. O app busca o catálogo na API.
2. A API retorna todas as figurinhas.
3. O usuário marca no app quais figurinhas possui.
4. O app salva a quantidade localmente.
5. A API continua responsável apenas pelos dados oficiais do álbum.

---

## Como executar testes manuais

Acesse a documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

Ou, após deploy:

```text
https://sua-api.vercel.app/docs
```

Teste os endpoints principais:

```text
GET /
POST /figurinhas
POST /figurinhas/lote
GET /figurinhas
GET /figurinhas/{id}
GET /figurinhas/numero/{numero_album}
GET /figurinhas/pais/{pais}
PUT /figurinhas/{id}
DELETE /figurinhas/{id}
```

---

## Autor

João Pedro Silva da Rosa Lima

Projeto desenvolvido como parte do aplicativo **Álbum da Copa**, com o objetivo de permitir o gerenciamento de figurinhas da Copa de forma simples, organizada e escalável.