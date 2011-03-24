
server {
	listen 80;
	listen 443 ssl;
	server_name static.civicboom.com;
	root /var/www/cb-static/;
	expires max;
	add_header Cache-Control public;
}

server {
	listen 80;
	listen 443 ssl;
	server_name civicboom-static.s3.amazonaws.com civicboom-static-test.s3.amazonaws.com;
	root /tmp/warehouse/;
}
