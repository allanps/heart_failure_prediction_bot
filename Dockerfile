FROM python:3.10-slim

COPY assets /app/assets

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY model_pipeline.py /app/model_pipeline.py
COPY main.py /app/main.py

CMD sh -c "python /app/model_pipeline.py && python /app/main.py"
