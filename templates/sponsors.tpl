{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}

{% with sponsors = conference.sponsors %}
{% include 'sponsor_block.tpl' %}
{% endwith %}

{% endblock%}