FROM python:2.7-alpine
LABEL maintainer="boubouh.karim@gmail.com"
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# ADD . /vcar
COPY ./requirements2.txt /vcar/requirements2.txt
WORKDIR /vcar
RUN pip install -r requirements2.txt
CMD ["python", "manage.py"]