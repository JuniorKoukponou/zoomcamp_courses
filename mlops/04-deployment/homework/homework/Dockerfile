FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip
RUN pip install pipenv

RUN mkdir -p /app/output

WORKDIR /app


COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["scoring.py", "./"]

EXPOSE 9696

ENTRYPOINT ["python", "scoring.py", "--year=2023", "--month=5"]

# docker build -t ride-duration-prediction-batch:v1 .
# docker run -it --rm -p 9696:9696  ride-duration-prediction-batch:v1
