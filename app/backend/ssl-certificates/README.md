#How to create an ssl certificate

####For development use:

Ref: http://kracekumar.com/post/54437887454/ssl-for-flask-local-development

Generate a private key:

`openssl genrsa -des3 -out server.key 1024`

Generate a CSR:

`openssl req -new -key server.key -out server.csr`

Remove Passphrase from key:

`cp server.key server.key.org`

`openssl rsa -in server.key.org -out server.key`

Generate self signed certificate:

`openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`


###For production use:

ref: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https