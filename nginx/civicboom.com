# vim:ft=conf

# cache_path needs to be set globally, it doesn't work per-server :(
proxy_cache_path /tmp/osm-cache   levels=2:2 keys_zone=osm:1g inactive=30d;
proxy_cache_path /tmp/nginx-cache levels=2:2 keys_zone=cb:50m inactive=3m;
proxy_temp_path  /tmp/nginx-temp;

upstream backends {
	### START MANAGED BY DEBCONF
	# debconf will remove anything between the start and end
	# markers and replace with the configured list of backend
	# servers. Here we have a default so that the config file
	# works without being debconf'ed.
	server 127.0.0.1:5000;
	### END MANAGED BY DEBCONF
}

server {
	# server stuff
	listen 80;
	listen 443 default ssl;
	server_name .civicboom.com localhost _;
	access_log /var/log/nginx/civicboom.log;
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
	proxy_pass_header Set-Cookie;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Url-Scheme $scheme;

	# by default, proxy to pylons
	location / {
		proxy_cache "cb";
		proxy_cache_key "$scheme://$host$request_uri-cookie:$cookie_civicboom_logged_in";
		proxy_pass http://backends;
	}

	# for tiles, proxy to openstreetmap
	# (this allows HTTPS, and caching for offline demos)
	location /misc/tiles/ {
		expires 30d;
		proxy_cache "osm";
		proxy_cache_key "$request_uri";
		proxy_set_header Host tile.openstreetmap.org;
		proxy_pass http://tile.openstreetmap.org/;
	}
}

# for demo-mode, we need a local "static" server, because demo avatar
# URLs are hardcoded as http://static.civicboom.com/public/blahblah.png
server {
	listen 80;
	listen 443 ssl;
	server_name static.civicboom.com civicboom-static.s3.amazonaws.com civicboom-static-test.s3.amazonaws.com;
	root /tmp/warehouse/;
	location /public/ {
		alias /opt/cb/share/website/civicboom/public/;
	}
}
