FROM python:3.13.4-slim-bullseye

RUN apt-get update && apt-get install -y curl

#Creare a virtual environment
RUN python -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app

#COPY local_folder/file container_destination
COPY requirements.txt /tmp/requiremments.txt

#RUN within_container_while_building
RUN pip install -r /tmp/requiremments.txt

COPY ./src .

CMD ["python","-m","http.server","8000"]