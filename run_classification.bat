docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
cd classification && python server.py