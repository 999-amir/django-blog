{% extends 'mail_templated/base.tpl' %}

{% block subject %}
activate and verify
{% endblock %}

{% block html %}
<h1>Hello {{ name }}✋✋✋<br>click below to activate your user</h1>
<h4>⛔ if you don't send request to site, it may be someone want to make access to your-page (don't click below) ⛔</h4>
<a href="{{ host }}{{ link }}">verify</a>
{% endblock %}