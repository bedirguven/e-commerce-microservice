FROM rabbitmq:3-management

# RabbitMQ yapılandırma dosyasını kopyala
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# Tanımlar (queue, exchange, binding vb.) dosyasını kopyala
COPY definitions.json /etc/rabbitmq/definitions.json

# RabbitMQ, başlangıçta tanımlar dosyasını yüklesin
ENV RABBITMQ_LOAD_DEFINITIONS=/etc/rabbitmq/definitions.json