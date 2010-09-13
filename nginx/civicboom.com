# vim:ft=conf

# cache_path needs to be set globally, it doesn't work per-server :(
proxy_cache_path /tmp/nginx-cache levels=2:2 keys_zone=cb:10m;
proxy_temp_path  /tmp/nginx-temp;

server {
	# server stuff
	listen 80;
	listen 443 default ssl;
	server_name .civicboom.com new-server localhost;
	access_log /var/log/civicboom/nginx.log;
	root /opt/cb/share/website/civicboom/public/;
	error_page 500 502 503 504 /errors/50x.html;
	client_max_body_size 25m;
	ssi on;

	# ssl
	ssl_certificate      /opt/cb/etc/ssl/civicboom.com.crt;
	ssl_certificate_key  /opt/cb/etc/ssl/civicboom.com.key;

	# gzip
	gzip on;
	gzip_disable "MSIE [1-6]\.(?!.*SV1)";
	gzip_types text/plain text/css application/javascript; # text/html is implied

	# proxy settings
	proxy_cache "cb";
	proxy_cache_key  "$scheme://$host$request_uri-cookie:$cookie_civicboom_logged_in";
	proxy_pass_header Set-Cookie;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Url-Scheme $scheme;
	if ($http_host ~  "(localhost|new-server)") {set $proxy_port 5000;}
	if ($http_host !~ "(localhost|new-server)") {set $proxy_port 5080;}

	# for all requests that start with / (ie, all requests), proxy to pylons
	location / {proxy_pass http://127.0.0.1:$proxy_port$uri$is_args$args;}
}
