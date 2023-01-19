openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out signreq.csr
openssl x509 -req -days 365 -in signreq.csr -signkey key.pem -out certificate.pem
openssl x509 -text -noout -in certificate.pem
