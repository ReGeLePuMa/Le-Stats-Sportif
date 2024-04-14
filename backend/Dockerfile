FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY nutrition_activity_obesity_usa_subset.csv nutrition_activity_obesity_usa_subset.csv
RUN pip install -r requirements.txt
COPY app/ .
EXPOSE 5000
ENV FLASK_APP=routes
CMD ["flask", "run", "--host", "0.0.0.0"]
