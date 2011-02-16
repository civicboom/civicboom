# vim:ft=conf

# more brokenness on 64-bit, needs to be fixed upstream
server_names_hash_bucket_size 64;

# cache_path needs to be set globally, it doesn't work per-server :(
proxy_cache_path /tmp/osm-cache   levels=2:2 keys_zone=osm:200m inactive=30d;
proxy_cache_path /tmp/nginx-cache levels=2:2 keys_zone=cb:50m inactive=3m;
proxy_temp_path  /tmp/nginx-temp;

log_format timing '$remote_addr - $remote_user [$time_local] "$request" $status $bytes_sent $upstream_response_time $request_time';

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
	listen 80;                listen [::]:80 ipv6only=on;
	listen 443 default ssl;   listen [::]:443 default ssl ipv6only=on;
	server_name .civicboom.com localhost _;
	access_log /var/log/nginx/civicboom.log;
	access_log /var/log/nginx/civicboom.timing.log timing; # DC_TIMING
	root /opt/cb/share/website/civicboom/public/;
	error_page 500 502 503 504 /errors/50x.html;
	client_max_body_size 100m;
	ssi on;

	# ssl
	ssl_certificate      /opt/cb/etc/ssl/wild.civicboom.com.pem;
	ssl_certificate_key  /opt/cb/etc/ssl/wild.civicboom.com.key;

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
		# $request_uri is what the browser sends, $uri is the currently active
		# request. This is important when using SSI, as all subrequests have
		# the same $request_uri and so they clobber eachother in the cache store.
		#
		# DC_CACHING lines are removed by debconf if caching = false
		proxy_cache "cb"; # DC_CACHING
		proxy_cache_key "$scheme://$host$uri-cookie:$cookie_civicboom_logged_in"; # DC_CACHING
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

	# for errors, don't proxy to pylons, just serve static files
	location /errors/ {
	}

	location /nginx_status {
		stub_status on;
		access_log   off;
		allow 127.0.0.1;
		allow 212.110.185.0/24;
		allow 129.12.0.0/16;
		allow 192.168.0.0/16;
		deny all;
	}
}

server {
	listen 80;
	listen 443 ssl;
	server_name static.civicboom.com;
	root /opt/cb/share/website/civicboom/public/;
}

server {
	listen 80;
	listen 443 ssl;
	server_name civicboom-static.s3.amazonaws.com civicboom-static-test.s3.amazonaws.com;
	root /tmp/warehouse/;
}
