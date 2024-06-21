FROM python:3.12.2

WORKDIR /api

COPY . /api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "api.py"]