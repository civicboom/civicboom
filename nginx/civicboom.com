# vim:ft=conf

server {
	# server stuff
	listen 80;
	listen 443 default ssl;
	server_name .civicboom.com new-server;
	access_log /var/log/civicboom/nginx.log;
	error_page 500 502 503 504 /errors/50x.html;

	# ssl
	ssl_certificate      /opt/cb/etc/ssl/civicboom.com.crt;
	ssl_certificate_key  /opt/cb/etc/ssl/civicboom.com.key;

	# gzip
	gzip on;
	gzip_disable "MSIE [1-6]\.(?!.*SV1)";
	gzip_types text/plain text/css application/x-javascript; # text/html is implied


	# ideally this would be
	#   location /         {[static files]; error_page 404 = @memcache}
	#   location @memcache {[memc config];  error_page 404 = @pylons}
	#   location @pylons   {[pylons config]}
	# but it seems that 404 handlers can't be chained :(
	# as a result, things that would go in @memcache are in if(file not on disk) {}

	location / {
		rewrite ^/$ /misc/titlepage;
		root /opt/cb/share/website/civicboom/public/;
		default_type text/html;

		# if a file exists on disk, serve from disk
		if (-e $request_filename) {
			expires 1y;
			add_header Cache-Control public;
		}

		# if a file does not exist on disk, serve from memcache
		if (!-e $request_filename) {
			set $memcached_key uri:$request_uri;
			memcached_pass 127.0.0.1:11211;
		}

		# if no file, and no memcache, try pylons
		error_page 404 = @pylons;
	}

	location @pylons {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Url-Scheme $scheme;
		proxy_pass       http://127.0.0.1:5080;
	}
}

server {
	listen 80;
	server_name localhost;
	access_log /var/log/civicboom/nginx.log;

	location / {
		rewrite ^/$ /misc/titlepage;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_pass       http://127.0.0.1:5000;
	}
}
