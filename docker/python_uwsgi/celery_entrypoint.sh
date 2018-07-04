#!/bin/sh


if [ -f "$CELERY_PID_FILE" ]
then
	echo "Deleting celery pid file: $CELERY_PID_FILE"
	rm -f ${CELERY_PID_FILE}
fi

chown -R www-data:www-data /data
chmod -R 0777 /data

exec "$@"