FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY dist/ dist/
COPY server.py server.py
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "server.py"]