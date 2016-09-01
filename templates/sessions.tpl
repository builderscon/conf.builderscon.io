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

div.speaker-avatar {
    text-align: center;
}
img.speaker-avatar {
    margin: 5px auto 2px auto;
    width: 80px;
    height: 80px;
    border: 1px solid #ccc;
}

table.session-info td {
    font-size: 70%;
    padding: 2px !important;
}

.session-list>div:nth-child(odd) {
	background-color: white;
}

.session-list>div:nth-child(even) {
	background-color: #f1f1f1;
}

.session-label {
	background-color: #9e9e9e;
}

.speaker-label>a {
	color  : white;
}

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


{% macro session_item(session, speaker, conference) %}
  <div class="small-3 large-3 columns">
    <div class="speaker-avatar"><img class="speaker-avatar" src="{{ speaker.avatar_url }}"/></div>
  </div>
  <div class="small-9 large-9 columns">
    <div>
      <h4><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a></h4>
      <div><a href="/user/{{ speaker.id }}">{{ speaker.nickname }}</a></div>
    </div>
  </div>
{% endmacro %}

{% macro session_list(sessions, title) %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{ title }}</h1>
      <div class="section-content sessions-container">
        {{ list_description(title) }}
        <div class="session-list row">
{% for session in sessions %}
{% if loop.index0 % 2 == 0 %}
          <div class="row">
{% endif %}
            <div class="large-6 columns">
                {{ session_item(session, session.speaker, conference) }}
            </div>
{% if loop.index0 % 2 == 1 or loop.last %}
          </div>
{% endif %}
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
