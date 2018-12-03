#!/bin/sh

#/usr/bin/supervisord -n -c /etc/supervisord.conf
/usr/bin/supervisord -c /etc/supervisord.conf
nginx -g 'daemon off;'