FROM alpine:3.9 as alpine-systemd

RUN 

RUN apk update && \
    apk add --no-cache openssh-server && \
    rm -rf /var/cache/apk/*

# Copy SSH keys
COPY secrets/id_rsa.pub /root/.ssh/authorized_keys

# Copy custom Nginx configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80 2226