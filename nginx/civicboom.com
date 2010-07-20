server {
	listen   80;
	listen   443 default ssl;
	server_name  .civicboom.com new-server localhost;
	access_log  /var/log/civicboom/nginx.log;
	ssl_certificate      /opt/cb/etc/ssl/civicboom.com.crt;
	ssl_certificate_key  /opt/cb/etc/ssl/civicboom.com.key;

	location / {
		# static files
		root   /opt/cb/share/website/civicboom/public/;
		error_page   404  /404.html;
		error_page   500 502 503 504  /50x.html;

		# if it's not a static file, let pylons handle it
		rewrite ^/$ /misc/titlepage;
		proxy_set_header  Host $host; 
		proxy_set_header  X-Real-IP $remote_addr; 
		proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for; 
		if (!-e $request_filename) {
			proxy_pass        http://127.0.0.1:5080;
		}
	}
}
