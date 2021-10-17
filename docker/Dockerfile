#Dockerfile

FROM python:3.9.2-alpine3.13
#COPY demo_app /app
COPY frontend /app
RUN apk add curl
WORKDIR /app
RUN chmod +x start.sh
RUN ./start.sh
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip3 install -r requirements.txt
EXPOSE 8080
#ENTRYPOINT ["/bin/sh", "start.sh"]
ENTRYPOINT ["python"]

CMD ["app.py"]
