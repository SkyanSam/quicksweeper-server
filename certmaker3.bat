openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout key.pem -out certificate.pem -config san.cnf
openssl x509 -in cert.pem -text -noout