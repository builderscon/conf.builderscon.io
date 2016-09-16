{% extends 'layout/base.tpl' %}

{% block body_id %}conference{% endblock %}

{% block menuitems %}
<li><a href="/">{% trans %}builderscon{% endtrans %}</a></li>
<li><a href="/dashboard">{% trans %}Dashboard{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}">{% trans %}Conference{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}/sessions">{% trans %}Sessions{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}/news">{% trans %}NEWS{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}/sponsors">{% trans %}SPONSORS{% endtrans %}</a></li>
{% endblock %}