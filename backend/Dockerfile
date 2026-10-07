FROM python:3.12-slim AS dependencies

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --no-create-home app

COPY --from=dependencies /install /usr/local
COPY --chown=app:app . .

USER app

EXPOSE 5001

CMD ["sh", "-c", "python -c 'from app import prepare_application; prepare_application()' && exec gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 1 --threads 4 app:app"]
