<%inherit file="base.mako"/>
<%def name="title()">${_("Developer Terms and Conditions for API")}</%def>

<b>Developer Terms and Conditions for API (Application Programming Interface):</b>
<p>If you are a developer or operator of a Platform application or website, the following additional terms apply to you:
<p>You are responsible for your application and its content and all uses you make of this API. This includes ensuring your application or use of Platform meets our Developer Terms and Conditions as set out here.
<p>Your access to and use of data you receive from Civicboom will be limited as follows:

<ol class='legal'>
<li>You will only request data you need to operate your application
<li>You will have a privacy policy that tells users what user data you are going to use and how you will use, display, share, or transfer that data and you will include your privacy policy URL in the Developer Application.
<li>You will not use, display, share, or transfer a user’s data in a manner inconsistent with your privacy policy.
<li>You will delete all data you receive from us concerning a user if the user asks you to do so, and will provide a mechanism for users to make such a request.
<li>You will not include data you receive from us concerning a specific identifiable user in any advertising creative.
<li>You will not sell user data. If you are acquired by or merge with a third party, you can continue to use user data within your application, but you cannot transfer user data outside of your application.
<li>We can require you to delete user data if you use it in a way that we determine is inconsistent with users’ expectations.
<li>We can limit your access to data.
<li>You will make it easy for users to remove or disconnect from your application.
<li>You will make it easy for users to contact you.
<li>You will provide customer support for your application.
<li>We give you all rights necessary to use the code, APIs, data, and tools you receive from us.
<li>You will not sell, transfer, or sublicense our code, APIs, or tools to anyone.
<li>You will not misrepresent your relationship with Civicboom to others.
<li>You may use the logos we make available to developers or issue a press release or other public statement so long as you follow these Developer Terms and Conditions.
<li>We can issue a press release describing our relationship with you.
<li>You will comply with all applicable laws
<li>You give us all rights necessary to enable your application to work with Civicboom
<li>You give us the right to link to or frame your application, and place content around your application.
<li>We can analyse your application, content, and data for any purpose.
<li>To ensure your application is safe for users, we can audit it.
</ol>

<p>Last updated January 2011.


<%def name="breadcrumbs()">
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
		<span itemprop="title">About</span>
	</a>
</span>
&rarr;
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
		<span itemprop="title">Legal</span>
	</a>
</span>
</%def>
