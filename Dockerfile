FROM python:3.10-alpine

WORKDIR Bot_Track

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .

CMD [ "python3", "app.py", "--host=0.0.0.0"]