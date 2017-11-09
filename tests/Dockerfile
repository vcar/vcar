FROM alpine
LABEL maintainer="boubouh.karim@gmail.com"
RUN apk update && apk add nodejs 
RUN mkdir average
ADD average.js average/
WORKDIR average
# ADD # copies new files, directories or remote file to container.
# CMD [ "node", "average.js" ] # You can overide the cmd (bin/sh -c) 
# CMD ping google.com
ENTRYPOINT [ "node", "average.js" ] # You can't (no shell && pid 1 && passed are arguments)
# ONBUILD # adds a trigger instruction when the image is used as the base for another build.
