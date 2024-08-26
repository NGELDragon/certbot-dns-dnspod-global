# certbot-dns-dnspod-global
certbot-dns-dnspod-global,  api.dnspod.com

# Installing
```linux
pip install git+https://github.com/NGELDragon/certbot-dns-dnspod-global.git
```

# INI File
```ini
# /etc/letsencrypt/dnspod.ini
dns_dnspod_api_id = "your-api-id"
dns_dnspod_api_token = "your-api-token"
```
# Certbot
```linux
sudo certbot certonly --authenticator dns-dnspod-global \
  --dns-dnspod-global-credentials /etc/letsencrypt/dnspod.ini \
  -d example.com -d "*.example.com"
```
