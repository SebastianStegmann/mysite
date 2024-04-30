FROM python:3.10.5
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python -m bottle --debug --reload app
