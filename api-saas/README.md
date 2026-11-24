# 🏢 SaaS B2B Admin API — Sistema Base

Backend administrativo responsável pela gestão de empresas clientes, assinaturas, saldos de créditos de API e trilha de auditoria de Customer Success (CS). Construído com **Python 3.12**, **FastAPI**, **SQLAlchemy**, **Alembic** e **PostgreSQL**, containerizado com **Docker** e **Docker Compose**.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado e configurado em seu ambiente:

* **Docker Engine** (versão 20.10 ou superior)
* **Docker Compose** (v2 ou superior — comando `docker compose`)
* **Git** (para clonar o repositório)
* **Portas livres no host:**
  * Porta **`8002`** disponível para a API FastAPI
  * Porta **`5434`** disponível para o banco de dados PostgreSQL
* *(Opcional)* **`uv`** instalado localmente, caso deseje gerenciar dependências ou rodar comandos fora do container
* *(Opcional)* **`curl`**, **Postman** ou navegador web para testar os endpoints

---

## 📁 Estrutura do Projeto

```text
saas-base-api/
├── alembic/
│   ├── versions/
│   │   └── 001_init_and_seed.py   # Criação das tabelas e carga inicial de dados
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── database.py                # Configuração de conexão SQLAlchemy
│   ├── main.py                    # Rotas e regras da API FastAPI
│   ├── models.py                  # Modelos ORM (Empresa, Assinatura, AuditoriaCS)
│   └── schemas.py                 # Schemas de validação Pydantic
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh                  # Script de inicialização (migrations + uvicorn)
└── pyproject.toml                 # Dependências gerenciadas via uv
```

---

## 🚀 Como Executar a Aplicação

### 1. Acesse o diretório do projeto
```bash
cd saas-base-api
```

### 2. Construa e suba os containers
Execute o comando abaixo para construir a imagem, instalar as dependências via `uv` e iniciar o PostgreSQL e a API em segundo plano:

```bash
docker compose up -d --build
```

> **Nota:** O script `entrypoint.sh` aguarda o PostgreSQL ficar saudável (`healthcheck`), executa automaticamente `uv run alembic upgrade head` (criando as tabelas e inserindo a massa de dados inicial) e inicia o servidor FastAPI na porta `8002`.

### 3. Verifique os logs de inicialização
Confirme se as migrations e o servidor subiram sem erros:

```bash
docker compose logs -f api
```

### 4. Valide o funcionamento da API
Teste o endpoint de saúde via terminal:

```bash
curl http://localhost:8002/health
```

**Resposta esperada:**
```json
{"status":"ok"}
```

### 5. Acesse a Documentação Interativa (Swagger UI)
Abra o navegador nos endereços abaixo para explorar e testar os endpoints:

* **Swagger UI:** `http://localhost:8002/docs`
* **ReDoc:** `http://localhost:8002/redoc`

---

## 🗄️ Massa de Dados Inicial (Seed)

Ao subir pela primeira vez, a migration `001_init_and_seed.py` popula automaticamente o banco com os seguintes registros para testes:

| Empresa ID | Nome Fantasia | CNPJ | Assinatura ID | Plano | Status | Saldo Inicial (Créditos) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | **Logística Sul** | `11.222.333/0001-44` | `10` | `STARTER` | `ATIVA` | `1200` |
| `2` | **TechFlow Soluções** | `22.333.444/0001-55` | `11` | `PRO` | `INATIVA` | `300` |
| `3` | **Alpha Varejo Brasil** | `33.444.555/0001-66` | `12` | `STARTER` | `ATIVA` | `500` |
| `4` | **Alpha Cloud Sistemas** | `44.555.666/0001-77` | `13` | `ENTERPRISE` | `ATIVA` | `10000` |

---

## 🔌 Endpoints Disponíveis e Exemplos de Uso

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/health` | Verifica a disponibilidade da API. |
| `GET` | `/empresas?nome={termo}` | Busca empresas cadastradas por filtro parcial no nome fantasia. |
| `GET` | `/assinaturas/{empresa_id}` | Retorna os dados da assinatura, status e saldo de créditos da empresa. |
| `POST` | `/assinaturas/{assinatura_id}/creditos` | Adiciona créditos extras a uma assinatura **ATIVA** e grava log de auditoria. |
| `PATCH` | `/assinaturas/{assinatura_id}` | Atualiza o plano e o limite de usuários da assinatura. |
| `GET` | `/auditoria-cs` | Lista o histórico de operações registradas na trilha de auditoria. |

### Exemplos rápidos via `curl`

* **Buscar empresa por nome:**
  ```bash
  curl "http://localhost:8002/empresas?nome=Logística"
  ```

* **Consultar assinatura da empresa (`empresa_id = 1`):**
  ```bash
  curl "http://localhost:8002/assinaturas/1"
  ```

* **Incluir créditos extras (`assinatura_id = 10`):**
  ```bash
  curl -X POST "http://localhost:8002/assinaturas/10/creditos" \
    -H "Content-Type: application/json" \
    -d '{"quantidade": 500, "motivo": "Bonificação por instabilidade técnica"}'
  ```

* **Consultar histórico de auditoria:**
  ```bash
  curl "http://localhost:8002/auditoria-cs"
  ```

---

## 🛠️ Comandos Úteis de Manutenção

* **Verificar status dos containers:**
  ```bash
  docker compose ps
  ```

* **Parar os containers mantendo os dados salvos no volume:**
  ```bash
  docker compose down
  ```

* **Resetar completamente o banco de dados (apaga o volume e recria o seed inicial):**
  ```bash
  docker compose down -v
  docker compose up -d --build
  ```
