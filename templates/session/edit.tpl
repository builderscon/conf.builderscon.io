{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
{% include 'session/form_header.tpl' %}
{% endblock %}

{% block scripts %}
{% include 'session/form_scripts.tpl' %}
{% endblock %}

{% block main %}
<main>
{% set action='/' + conference.full_slug + '/session/' + session.id + '/update' %}
{% with action=action, session=session, for_edit=True, video_url=True if flask_session.user.is_admin else False, slide_url=True %}
  {% include 'session/form.tpl' %}
{% endwith %}
</main>
{% endblock %}
