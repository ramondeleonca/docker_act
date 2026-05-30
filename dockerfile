FROM python:3.12-slim
WORKDIR /app
COPY app.py .
COPY templates/ templates/
COPY static/ static/
RUN pip install flask flask-sqlalchemy psycopg2-binary
EXPOSE 5000
CMD ["python", "app.py"]
