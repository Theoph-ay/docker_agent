# declare what image to use
# FROM accountname/imagename:tag
# FROM image_name:latest(tag)
FROM python:3.13.4-slim-bullseye

WORKDIR /app
#any other frontend app


#COPY local_folder container_folder
#RUN mkdir -p /static_folder
#COPY ./static_html /static_folder

COPY ./src /app
#COPY ./static_folder . same as above

#RUN echo "hello" > index.html #Linux command

#docker build -f Dockerfile -t pyapp .
#docker run -it pyapp

# docker build -f Dockerfile -t accountname/appname:tag .
# docker push accountname/appname:tag

# python -m http.server 8000
# docker run -d -p 3000:8000 pyapp 
CMD ["python","-m","http.server","8000"]