{% extends 'layout/base.tpl' %}

{% block body_id %}userview{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{ user.nickname }}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-2 small-2 columns">
            <div class="profile">
              <img src="{{ user.avatar_url or '/static/images/noprofile.png' }}">
              <p class="name">{{ user.nickname }} <span class="auth_via">{{ user.auth_via }}</span></p>
            </div>
          </div>
          <div class="profile-content large-10 small-10 columns">
{% if conferences %}
            <h3>{% trans %}Organizer{% endtrans %}</h3>
            <table class="conference-history">
            <thead>
              <tr>
                <td>{% trans %}Conference{% endtrans %}</td>
              </tr>
            </thead>
            <tbody>
{% for conference in conferences %}
              <tr>
                <td><a href="/{{ conference.full_slug }}">{{ conference.title }}</a></td>
              </tr>
{% endfor %}
            </tbody>
            </table>
{% endif %}

{% if sessions %}
            <h3>{% trans %}Past Sessions{% endtrans %}</h3>
            <table class="session-history">
            <tbody>
{% for session in sessions %}
              <tr>
                <td>{% with thumbnail = session | session_thumbnail_url %}{% if thumbnail %}<img class="video-thumbnail" src="{{ thumbnail }}">{% endif %}{% endwith %}</td>
                <td><span{% if session.conference.status == 'private' %} class="invalid"{% endif %}>{% if session.title %}<a href="/{{ session.conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a>{% else %}N/A{% endif %}</span></td>
                <td>{% if session.conference %}<a href="/{{ session.conference.full_slug }}">{{ session.conference.title }}</a>{% endif %}</td>
              </tr>
{% endfor %}
            </tbody>
            </table>
{% endif %}
          </div>
        </div>

      </div><!-- section-content -->
    </div><!-- inner -->
  </div><!-- section -->
</main>
{% endblock %}
