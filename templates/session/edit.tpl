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
{% if errors %}
<div class="box">
<div class="row box-header">
  <div class="col s12">{% trans %}Error{% endtrans %}</div>
</div>
<div class="row">
  <div class="col s12"><ul>{% for error in missing %}
    <li>{{ _("Missing field %s", error) }}</li>
  {% endfor %}</ul></div>
</div>
</div>
{% endif %}

{% set action='/' + conference.full_slug + '/session/' + session.id + '/update' %}
{% with action=action, session=session, for_edit=True, video_url=True if user.is_admin else False, slide_url=True %}
  {% include 'session/form.tpl' %}
{% endwith %}
</main>
{% endblock %}
