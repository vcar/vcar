FROM python:3-alpine
LABEL maintainer="boubouh.karim@gmail.com"

# Install required libraries
RUN apk add gcc python-dev musl-dev libffi-dev jpeg-dev zlib-dev linux-headers

# Setup nginx
RUN apk add nginx --no-cache
RUN adduser -D -g 'www' www
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig
COPY CONFIG/nginx/ /etc/nginx/
RUN mkdir -p /run/nginx
RUN nginx -t
RUN nginx -c /etc/nginx/nginx.conf

# Setup supervisor
RUN apk add supervisor
RUN mkdir -p /var/log/supervisor/vcar
RUN mkdir -p /var/log/vcar
RUN chmod -R 777 /var/log/vcar
COPY CONFIG/supervisor/supervisord.conf /etc/supervisord.conf
RUN supervisord -c /etc/supervisord.conf

# Install vCar
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 80

#CMD ["nginx", "-g", "daemon off;"]
CMD ["./cli/start.sh"]

#CMD ["ps"]
#CMD ["/var/log/nginx/debug.log"]
# CMD ["tail", "-f", "/var/log/nginx/debug.log"]
# CMD ["supervisorctl", "status"]
# CMD ["/bin/sh"]

#
#RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
#RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
## ADD . /vcar
#COPY ./requirements2.txt /vcar/requirements2.txt
#WORKDIR /vcar
#RUN pip install -r requirements2.txt
#CMD ["python", "manage.py"]