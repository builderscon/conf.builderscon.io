{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
.sessions-container {
    padding-left: 2em !important;
}

.speaker-name {
    text-align: center;
}

div.speaker-avatar {
    text-align: center;
}
img.speaker-avatar {
    margin: 5px auto 2px auto;
    width: 100px;
    height: 100px;
    border: 1px solid #ccc;
}

table.session-info td {
    font-size: 70%;
    padding: 2px !important;
}
-->
</style>
{% endblock %}

{% macro list_description(title) %}
{% if title == _('Pending Proposals') %}
<div>
{% trans %}These proposals have not yet been accepted for this conference. If you would like to see them in the conference, please help by sharing them on other media, as the number of shares will be taken into consideration when selection takes place{% endtrans %}
</div>
{% endif %}
{% endmacro %}

{% macro session_list(sessions, title) %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{ title }}</h1>
      <div class="section-content sessions-container">
        {{ list_description(title) }}
        <div class="session-list">
{% for session in sessions %}
        <div class="row session">
          <div class="large-2 columns">
{% with speaker = session.speaker %}
            <div class="speaker-avatar"><img class="speaker-avatar" src="{{ speaker.avatar_url }}"/></div>
          </div>
          <div class="large-10 columns">
            <h4><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a></h4>
            <div>
              <span class="label speaker-label">{% trans %}Speaker{% endtrans %}&#58; <a href="/user/{{ speaker.id }}">{{ speaker.nickname }}</a></span>
{% endwith %}
{% with conference = session.conference %}
              <span class="label session-label">{% trans %}Material Level{% endtrans %}&#58; {{ _(session.material_level|audlevelname) }}</span>
              <span class="label session-label">{% trans %}Duration{% endtrans %}&#58; {{ _(session.session_type.name) }}</span>
              <span class="label session-label">{% trans %}Spoken Language{% endtrans %}&#58; {{ _(session.spoken_language|langname) }}</span>
{% endwith %}
            </div>
          </div>
        </div>
{% endfor %}
        </div>
      </div>
    </div>
  </div>
{% endmacro %}

{% block main %}
<main>
{{ session_list(accepted_sessions, _('Accepted Sessions')) }}
{{ session_list(pending_sessions, _('Pending Proposals')) }}
</main>
{% endblock%}
