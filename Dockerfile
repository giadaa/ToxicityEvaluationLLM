FROM python:3.9.6-slim-buster

RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /bias-evaluation-app

ADD src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER app_user

COPY . .

CMD [ "python3", "src/main.py"]