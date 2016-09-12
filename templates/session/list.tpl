{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% macro list_description(title) %}
{% if title == _('Pending Proposals') %}
<div class="description-pending">
{% trans %}These proposals have not yet been accepted for this conference. If you would like to see them in the conference, please help by sharing them on other media, as the number of shares will be taken into consideration when selection takes place{% endtrans %}
</div>
{% endif %}
{% endmacro %}


{% macro session_item(session, speaker, conference) %}
<div class="large-6 columns session">
  <div class="small-3 large-3 columns">
    <div class="speaker-avatar"><img class="speaker-avatar" src="{{ speaker.avatar_url or '/static/images/noprofile.png' }}"/></div>
    <div class="session-language">{{ session.spoken_language | upper }}</div>
  </div>
  <div class="small-9 large-9 columns">
    <div>
      <div class="session-title"><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title | truncate(30) }}</a></div>
      <div class="speaker-name">by <a href="/user/{{ speaker.id }}">{{ speaker.nickname }}</a></div>
    </div>
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
            {{ session_item(session, session.speaker, conference) }}
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
{% if accepted_sessions %}{{ session_list(accepted_sessions, _('Accepted Sessions')) }}{% endif %}
{% if pending_sessions %}{{ session_list(pending_sessions, _('Pending Proposals')) }}{% endif %}
</main>
{% endblock%}
