server {
	listen   80;
	listen   443 default ssl;
	server_name  .civicboom.com new-server;
	access_log  /var/log/civicboom/nginx.log;
	ssl_certificate      /etc/ssl/certs/ssl-cert-snakeoil.pem;
	ssl_certificate_key  /etc/ssl/private/ssl-cert-snakeoil.key;

	location / {
		# static files
		root   /home/shish/website/src/civicboom/public/;
		error_page   404  /404.html;
		error_page   500 502 503 504  /50x.html;

		# if it's not a static file, let pylons handle it
		proxy_set_header  Host $host; 
		proxy_set_header  X-Real-IP $remote_addr; 
		proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for; 
		if (!-e $request_filename) {
			proxy_pass        http://127.0.0.1:5000;
		}
	}
}
