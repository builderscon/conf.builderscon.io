{% extends 'layout/base.tpl' %}

{% block body_id %}conference{% endblock %}

{% block menuitems %}
<li><a href="/{{ slug }}"><span class="i-home"></span></a></li>
<li><a href="/{{ slug }}/news">{% trans %}NEWS{% endtrans %}</a></li>
<li><a href="/{{ slug }}/sponsors">{% trans %}SPONSORS{% endtrans %}</a></li>
{% endblock %}