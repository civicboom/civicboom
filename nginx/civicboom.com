# vim:ft=conf

upstream backends {
	### START MANAGED BY DEBCONF
	# debconf will remove anything between the start and end
	# markers and replace with the configured list of backend
	# servers. Here we have a default so that the config file
	# works without being debconf'ed.
	server 127.0.0.1:5000;
	### END MANAGED BY DEBCONF
}

log_format cb_timing   '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent $upstream_response_time $request_time p:$pipe';
log_format cb_combined '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"';

server {
	# server stuff
	listen 80  default;       listen [::]:80  default     ipv6only=on;
	listen 443 default ssl;   listen [::]:443 default ssl ipv6only=on;
	server_name *.civicboom.com;
	access_log /var/log/nginx/civicboom.log cb_combined;
	access_log /var/log/nginx/civicboom.timing.log cb_timing; # DC_TIMING
	root /opt/cb/share/website-web/;
	error_page 500 /errors/50x.html;
	error_page 502 /errors/502.html;
	error_page 503 /errors/503.html;
	error_page 504 /errors/504.html;
	client_max_body_size 100m;
	ssi on;

	# ssl
	ssl_certificate      /opt/cb/etc/ssl/wild.civicboom.com.pem;
	ssl_certificate_key  /opt/cb/etc/ssl/wild.civicboom.com.key;
	ssl_session_cache    shared:SSL:10m;
	ssl_session_timeout  10m;

	# normalise the environment
	set $cb_scheme $scheme;
	if ($http_x_forwarded_proto) {
		# if we are behind an amazon load balancer, we only see HTTP
		# with "https" stored in x-forwarded-proto
		set $cb_scheme $http_x_forwarded_proto;
	}

	set_real_ip_from   10.0.0.0/8;
	set_real_ip_from   192.168.0.0/16;
	set_real_ip_from   127.0.0.0/8;
	real_ip_header     X-Forwarded-For;

	# proxy settings
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Url-Scheme $cb_scheme;
	proxy_pass_header Set-Cookie;

	# redirect civicboom.com to www.civicboom.com
	if ($host = civicboom.com) {
		rewrite ^(.*) $cb_scheme://www.civicboom.com$1 permanent;
	}

	# redirect to https, unless things are whitelisted already
	set $cb_security_checked "fail";
	if ($cb_scheme = "https") {
		set $cb_security_checked "ok";
	}
	if ($host ~* "^(api|widget)") {
		set $cb_security_checked "ok";
	}
	if ($http_user_agent ~* "ELB-HealthChecker") {
		set $cb_security_checked "ok";
	}
	if ($remote_addr = "127.0.0.1") {
		set $cb_security_checked "ok";
	}
	if ($cb_security_checked != "ok") {
		rewrite ^(.*) https://$host$1 permanent;
	}

	# by default, proxy to pylons
	location / {
		# $request_uri is what the browser sends, $uri is the currently active
		# request. This is important when using SSI, as all subrequests have
		# the same $request_uri and so they clobber eachother in the cache store.
		proxy_cache "cb";
		proxy_cache_key "$cb_scheme://$host$uri$is_args$args-cookie:$cookie_logged_in";
		proxy_cache_bypass $cookie_nocache;
		proxy_pass http://backends;
	}

	# for tiles, proxy to openstreetmap
	# (this allows HTTPS, and caching for offline demos)
	location /misc/tiles/ {
		expires 30d;
		proxy_cache "osm";
		proxy_cache_key "$request_uri";
		proxy_set_header Host tile.openstreetmap.org;
		proxy_pass http://193.63.75.26/;
	}

	# for errors, don't proxy to pylons, just serve static files
	location /errors/ {
	}

	location /nginx_status {
		stub_status on;
		access_log  off;
		allow 127.0.0.1;
		allow 212.110.185.0/24;
		allow 129.12.0.0/16;
		allow 192.168.0.0/16;
		deny all;
	}
}
