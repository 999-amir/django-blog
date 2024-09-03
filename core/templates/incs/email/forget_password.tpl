{% extends 'mail_templated/base.tpl' %}

{% block subject %}
activate and verify
{% endblock %}

{% block html %}
<h1>Hello {{ name }}✋✋✋<br>forget your password? click below</h1>
<h4>⛔ if you don't send request to site, it may be someone want to make access to your-page (don't click below) ⛔</h4>
<a href="{{ host }}{{ link }}">verify</a>
{% endblock %}