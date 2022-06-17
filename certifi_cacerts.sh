domain=$1
openssl s_client -host "$domain" -port 443 -showcerts 2>/dev/null </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > .venv/lib/python3.9/site-packages/certifi/cacert.pem