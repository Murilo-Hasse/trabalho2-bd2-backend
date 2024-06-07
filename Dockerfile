FROM python:3.11.1

WORKDIR /trabalho2-bd2-backend

COPY requirements.txt ./

RUN python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    deactivate"

COPY . .

CMD ["/bin/bash", "-c", "source venv/bin/activate && exec python api.py"]

