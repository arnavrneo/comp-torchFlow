FROM tiangolo/uvicorn-gunicorn:python3.7

RUN apt-get update
RUN apt-get update && apt-get install libsm6 libxext6 -y


WORKDIR /appdir


COPY requirements.txt /appdir
RUN pip install --no-cache-dir -r /appdir/requirements.txt

COPY ./server /appdir

ENTRYPOINT ["python", "main.py"]