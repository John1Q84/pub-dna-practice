#Dockerfile

FROM python:3.9.2-alpine3.13
COPY demo_app /app
RUN apk add curl
WORKDIR /app
#RUN source v_demo_app/bin/activate
#RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["/bin/sh", "start.sh"]

#CMD ["app.py"]
