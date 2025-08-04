FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install -y libpq5  # for psycopg


ADD ./src /app/src
WORKDIR /app
COPY ./pyproject.toml /app
COPY ./uv.lock /app
RUN uv sync --locked


EXPOSE 8000
ENTRYPOINT ["uv"]
CMD ["run", "./src/manage.py", "runserver", "0.0.0.0:8000"]
