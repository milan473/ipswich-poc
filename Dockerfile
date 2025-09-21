FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate --noinput
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce.wsgi"]