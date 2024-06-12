FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy
# --system — Install packages to the system site-packages rather than into your virtualenv.
# --deploy — Verifies the _meta hash of the lock file is up to date with the ``Pipfile``, aborts install if not.

COPY ["predict.py", "./model/lin_reg.bin", "./"]

EXPOSE 9696:9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
