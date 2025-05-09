FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

CMD ["gunicorn", "feedback_report.wsgi", "--bind", "0.0.0.0:8000"]