FROM nginx

COPY ./nginx.conf /etc/nginx/nginx.conf
ADD ./keys/localhost+1.pem /etc/keys/localhost.pem
ADD ./keys/localhost+1-key.pem /etc/keys/localhost-key.pem

EXPOSE 443
