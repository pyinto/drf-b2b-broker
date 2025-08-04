set dotenv-load
set dotenv-required



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
