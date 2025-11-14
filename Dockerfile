FROM python:3.11-slim


# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/


EXPOSE 8000

CMD ["gunicorn", "tutorial.wsgi:application", "--bind", "0.0.0.0:8000"]