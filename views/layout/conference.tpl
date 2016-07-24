{% extends 'layout/base.tpl' %}

{% block menuitems %}
<li><a href="/{{ slug }}"><span class="i-home"></span></a></li>
<li><a href="/{{ slug }}/news">NEWS</a></li>
<li><a href="/{{ slug }}/sponsors">SPONSORS</a></li>
{% endblock %}