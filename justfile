set dotenv-load
set dotenv-required


BENCHMARK_QUERY_FINANCES_DIR := "./src/models/finances/tests/pgbench_queries"
BENCHMARK_OUTPUT_DIR := "./tmp/psqlbench"


@_default:
  echo "\n================================================= Commands ================================================\n"
  just --list --unsorted
  echo "\n===========================================================================================================\n"


# ------------ | Django | ------------
@manage *ARGS:
  python ./src/manage.py {{ARGS}}
startapp NAME:
  @mkdir -p './src/models/{{NAME}}/'
  just manage startapp '{{NAME}}' './src/models/{{NAME}}/'
makemigrations *APP:
  just manage makemigrations '{{APP}}'
migrate *APP:
  just manage migrate '{{APP}}'


# ------------ | Docker | ------------
docker-db:
  docker compose --profile 'db' up -d
docker-web:
  docker compose --profile 'web' up -d
docker-stop:
  docker compose --profile 'web' down --remove-orphans

docker-cmd *CMD:
  docker compose exec web {{CMD}}
docker-cmd-manage *CMD:
  just docker-cmd uv run /app/src/manage.py {{CMD}}
docker-migrate:
  just docker-cmd-manage migrate
docker-tests:
  just docker-cmd-manage test src --no-input


# ------------ | PSQL Benchmarks | ------------
@pgbench *CMD:
    pgbench                           \
        --host="${POSTGRES_HOST}"     \
        --port="${POSTGRES_PORT}"     \
        --dbname="${POSTGRES_DB}"     \
        --username="${POSTGRES_USER}" \
        {{CMD}}
pgbench-init:
  just pgbench --initialize
@pgbench-run-file FILE OUTPUT_NAME TIME="30" CLIENT="25" THREADS="10":
  just pgbench                     \
    --client={{CLIENT}}              \
    --jobs={{THREADS}}               \
    --time={{TIME}}                  \
    --protocol="prepared"            \
    --file="{{FILE}}"                \
    | tee "{{BENCHMARK_OUTPUT_DIR}}/{{OUTPUT_NAME}}.log"
#    --report-per-command
#    --progress=1  \

pgbench-tx-select CASE_NAME="reg":
  just pgbench-run-file "{{BENCHMARK_QUERY_FINANCES_DIR}}/tx-select.sql" "tx-select-"{{CASE_NAME}}
pgbench-tx-insert CASE_NAME="reg":
  just pgbench-run-file "{{BENCHMARK_QUERY_FINANCES_DIR}}/tx-insert.sql" "tx-insert-"{{CASE_NAME}}
pgbench-wallet-select CASE_NAME="reg":
  just pgbench-run-file "{{BENCHMARK_QUERY_FINANCES_DIR}}/wallet-select.sql" "wallet-select-"{{CASE_NAME}}
pgbench-wallet-insert CASE_NAME="reg":
  just pgbench-run-file "{{BENCHMARK_QUERY_FINANCES_DIR}}/wallet-insert.sql" "wallet-insert-"{{CASE_NAME}}

pgbench-all CASE_NAME="reg":
  just pgbench-init
  @echo "\n====================================|   Wallet    |===================================="
  just pgbench-wallet-insert {{CASE_NAME}}
  just pgbench-wallet-select {{CASE_NAME}}
  @echo "\n====================================| Transaction |===================================="
  just pgbench-tx-insert {{CASE_NAME}}
  just pgbench-tx-select {{CASE_NAME}}
