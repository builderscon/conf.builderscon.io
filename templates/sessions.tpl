{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
.sessions-container {
    margin-left: 2em !important;
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

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Sessions{% endtrans %}</h1>
      <div class="section-content sessions-container">
{% for session in sessions %}
{% with conference = session.conference %}
        <div class="row session">
          <div class="large-2 columns">
{% with speaker = session.speaker %}
            <div class="speaker-avatar"><img class="speaker-avatar" src="{{ speaker.avatar_url }}"/></div>
            <div class="speaker-name"><a href="/user/{{ speaker.id }}">{{ speaker.nickname }}</a></div>
{% endwith %}
          </div>
          <div class="large-10 columns">
            <h4><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a></h4>
<div class="row">
<div class="large-6 columns">
<table class="session-info">
<tr>
    <td>{% trans %}Starts On{% endtrans %}</td>
    <td>{{ session.starts_on or '-' }}</td>
</tr>
<tr>
    <td>{% trans %}Duration{% endtrans %}</td>
    <td>{{ _(session.session_type.name) }}</td>
</tr>
<tr>
    <td>{% trans %}Spoken Language{% endtrans %}</td>
    <td>{{ _(session.spoken_language|langname) }}</td>
</tr>
</table>
</div>
</div>
          </div>
        </div>
{% endwith %}
{% endfor %}
      </div>
    </div>
  </div>
</main>
{% endblock%}
