# Notes for certificate inspection and create certificate chain

## Inspect certificate chain
> openssl crl2pkcs7 -nocrl -certfile full-cert-chain.pem | openssl pkcs -print_certs -text -noout

## Build certificate chain
We generate 4096-bit RSA private keys for root, intermediate, and end with AES-256 encryption. Then we create new certificate signing request (CSR) for each of the root, intermediate and end certificate using their respective key. When creating the CSR, we also include information of the certificate such as Country, States, Location, Organisation and Common Name. After generating the CSR, we generate these 3 certificates using X509 standard with the validity of 365 days. The root certificate is self-signed with its own private key whereas the signing certificate and its corresponding private key (-CA, -CAkey) of intermediate certificate and end certificate are (root certificate, root private key) and (intermediate certificate, intermediate private key) respectively.

*Creating root certificate*
> sudo openssl genrsa -aes256 -out root_private.key 4096
> sudo openssl req -new -key root_private.key -out root.csr -subj "/C=VN/ST=JJ/L=GLB/O=USYD/CN=540849147 Root"
> sudo openssl x509 -req -in root.csr -out root.crt -signkey root_private.key -days 365

*Creating intermediate certificate signed by root CA*
> sudo openssl genrsa -aes256 -out intermediate_private.key 4096
> sudo openssl req -new -key intermediate_private.key -out intermediate.csr -subj "/C=VN/ST=JJ/L=GLB/O=USYD/CN=540849147 Intermediate"
> sudo openssl x509 -req -in intermediate.csr -CA root.crt -CAkey root_private.key -CAcreateserial -out intermediate.crt -days 365

*Creating end certificate signed by intermediate CA*
> sudo openssl genrsa -aes256 -out end_private.key 4096
> sudo openssl req -new -key end_private.key -out end.csr -subj "/C=VN/ST=JJ/L=GLB/O=USYD/CN=540849147 End"

*Concatenating 3 certificates into one*
> cat root.crt intermediate.crt end.crt > full-cert-chain.pem
