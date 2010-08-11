# vim:ft=conf

server {
	# server stuff
	listen 80;
	listen 443 default ssl;
	server_name .civicboom.com new-server localhost;
	access_log /var/log/civicboom/nginx.log;
	error_page 500 502 503 504 /errors/50x.html;
	root /opt/cb/share/website/civicboom/public/;

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
		# rewrite rules
		rewrite ^/$ /misc/titlepage;

		# if a file exists on disk, serve from disk
		if (-e $request_filename) {
			expires 1y;
			add_header Cache-Control public;
		}

		# if
		#   the file does not exist on disk
		#   the request method is GET or HEAD
		#   there are no cookies
		# try memcache
		default_type text/html;
		set $test "";
		if (!-e $request_filename)           {set $test "${test}F";} # nginx has no if(a && b) {}
		if ($request_method ~ "(GET|HEAD)" ) {set $test "${test}M";}
		if ($http_cookie = "" )              {set $test "${test}C";}
		if ($test = FMC) {
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
		if ($http_host ~ "(localhost|new-server)") {
			proxy_pass       http://127.0.0.1:5000;
		}
		if ($http_host !~ "(localhost|new-server)") {
			proxy_pass       http://127.0.0.1:5000;
		}
	}
}
