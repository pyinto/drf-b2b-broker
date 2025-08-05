## Instructions

### Docker Setup 🐳

#### 1. Configure Environment Variables.
```sh
cp .env.example .env && vim .env
```
#### 2. Run Docker Containers.
```sh
docker compose --profile 'web' up -d
```
#### 3. Apply Migrations.
```sh
docker compose exec 'web' uv run /app/src/manage.py migrate
```
#### 4. Create superuser.
```sh
docker compose exec 'web' uv run /app/src/manage.py createsuperuser
```
#### 5. Populate test data into DB.
```sh
docker compose exec 'web' uv run /app/src/manage.py generate_data --wallets-count 10 --tx-range 100 1000
```
#### 6. Browse APIs.
```sh
open "http://localhost:8000/api/v1/finances/transactions/"
```
#### 7. Run Tests.
```sh
docker compose exec 'web' uv run /app/src/manage.py test src --no-input 
```
---

### Local Django + Docker DB:
#### 1. Configure Environment Variables.
```sh
cp .env.example .env && vim .env
```
#### 2. Run db (PSQL) Docker Container.
```sh
docker compose --profile 'db' up -d
```
#### 3. Install venv && requirements by using [UV](https://docs.astral.sh/uv/).
```sh
uv sync
source .venv/bin/activate
```
#### 3. Apply Migrations.
```sh
python ./src/manage.py migrate
```
#### 4. Create superuser.
```sh
python ./src/manage.py createsuperuser
```
#### 5. Populate test data into DB.
```sh
python ./src/manage.py generate_data --wallets-count 10 --tx-range 100 1000
```
#### 6. Browse APIs.
```sh
open "http://localhost:8000/api/v1/finances/transactions/"
```
#### 7. Run Tests.
```sh
python ./src/manage.py test src --no-input
```

---

### Run PSQL Benchmarks 
#### 1. Make sure you have `pgbench (17.5)` installed.
```sh
pgbench -V
```

#### 2. Run Benchmarks by using [Justfile](https://github.com/casey/just).
```
just pgbench-all
```
#### 2.1. Or run directly by using next cmd.
```shell
BENCHMARK_QUERY_FINANCES_DIR="./src/models/finances/tests/pgbench_queries"

# Only on first run:
pgbench --initialize

pgbench                                                          \
	--client=10                                              \
	--jobs=3                                                 \
	--time=30                                                \
	--protocol="prepared"                                    \
	--progress=1                                             \
	--file="${BENCHMARK_QUERY_FINANCES_DIR}/tx-insert.sql"
```

---

---

---

## Requirements
Develop REST API server using **django-rest-framework** with pagination, sorting and filtering for two models:

### DB Models:
- **Wallet**
	- `id`
	- `label` *(is a string field)*
	- `balance` *(a summary of all transactions's amounts; balance should NEVER be negative)*

- **Transaction**
	- `id`
	- `wallet_id` *(fk)*
	- `txid` *(required unique string field)*
	- `amount` *(number with 18-digits precision; amount may be negative)*


> Where **txid** is required unique string field, **amount** is a number with 18-digits precision, **label** is a string field, **balance** is a summary of all transactions's amounts. Transaction amount may be negative. Wallet balance should NEVER be negative

### Tech Stack:
- **Python**: `3.11+`
- **Database**: `MySQL` or `Postgres`
- **Frameworks**: `django-rest-framework`
- **API specification:** [JSON:API](https://jsonapi.org/format/) *(you are free to use [this](https://django-rest-framework-json-api.readthedocs.io/en/stable/) library)*

### Will Be Your Advantage:
- [ ] Test coverage
- [ ] Any linter usage
- [ ] Quick start app guide if you create your own docker-compose or Dockerfiles
- [ ] Comments in non-standart places in code
- [ ] Use database indexes if you think it's advisable
