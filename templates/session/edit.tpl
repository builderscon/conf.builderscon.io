{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
{% include 'session/form_header.tpl' %}
{% endblock %}

{% block main %}
<main>
{% with action='/session/update', for_edit=True, video_url=True if flask_session.user.is_admin else False, slide_url=True %}
  {% include 'session/form.tpl' %}
{% endwith %}
</main>
{% endblock %}
