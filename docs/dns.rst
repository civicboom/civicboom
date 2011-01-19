DNS Notes
=========

host
  main
    alias

bytemark VM
  www.         main site
	mobile.    mobile view, defaults to format=mobile-html
	  m.       short alias
	widget.    widget view, defaults to format=widget-html
	  w.       short alias
    api-v1.    separate domain for API calls so they can be pointed to a different server later
	static.    a domain that only serves /public and has no cookies

office
  dev.         dev server
    new.       dev server proxies this to dev-ran, shish's development VM

google
  mail.        web interface
  smtp.
  imap.
  MX

