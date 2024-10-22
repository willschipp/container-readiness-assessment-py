## Install Ngninx

`sudo apt install nginx -y`

## Update Reverse Proxy
1. `sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bk`
2. edit the `nginx.conf` file to have the reverse proxy in it
3. test with `sudo nginx -t`
4. apply `sudo systemctl restart nginx`