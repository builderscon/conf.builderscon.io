{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
{% include 'session/form_header.tpl' %}
{% endblock %}

{% block main %}
<main>
{% with action='/session/update', for_edit=True %}
  {% include 'session/form.tpl' %}
{% endwith %}
</main>
{% endblock %}
