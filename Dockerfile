FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . .

RUN SECRET_KEY=temp-build-key ALLOWED_HOSTS=localhost DATABASE_URL=sqlite:///db.sqlite3 python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn wsgi_entry:application --bind 0.0.0.0:8080 --workers 2 --log-level debug"]