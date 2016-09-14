{% extends 'layout/base.tpl' %}

{% block body_id %}conference{% endblock %}

{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="/dashboard"><span class="i-user"></span></a></li>
<li><a href="/{{ full_slug }}"><span class="i-blackboard"></span></a></li>
<li><a href="/{{ full_slug }}/sessions">{% trans %}Sessions{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}/news">{% trans %}NEWS{% endtrans %}</a></li>
<li><a href="/{{ full_slug }}/sponsors">{% trans %}SPONSORS{% endtrans %}</a></li>
{% endblock %}