# kafka Text Sender

This is a simple messaging applicationg comprised of a typescript frount end with a kafa backend.

To run the application using docker run the following command:

`docker-compose --env-file kafka_settings.env up --build`

You should then be able to see three containers when you run `docker ps`

```
CONTAINER ID   IMAGE                      COMMAND                  CREATED        STATUS              PORTS                                                  NAMES
77a5dc166ee0   kafka_text_sender_web      "python app/app.py"      46 hours ago   Up 2 minutes        0.0.0.0:5000->5000/tcp                                 kafka_text_sender_web_1
262756b854cd   bitnami/kafka:latest       "/opt/bitnami/script…"   47 hours ago   Up About a minute   0.0.0.0:9092->9092/tcp                                 kafka_text_sender_kafka_1
cf72db5338be   bitnami/zookeeper:latest   "/opt/bitnami/script…"   2 days ago     Up 2 minutes        2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   kafka_text_sender_zookeeper_1
```

If there is an error similar to: Error while creating ephemeral at /brokers/ids/1001, node already exists and owner '<id>' does not match current session '<id>' run `docker-compose rm -svf` before running the docker compose command.

When the three containers have spun up navigate to `localhost:5000` to see the project root.

For deving:
`npm install -g npm@latest` -> node packages, `npm run watch`, start dev server `flask run`  
