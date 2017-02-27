{% extends 'layout/base.tpl' %}

{% block body_id %}dashboard{% endblock %}

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
              <a href="/user/{{ user.id }}" class="alert button profile-btn">{% trans %}Public Profile{% endtrans %}</a>
              <form action="/user/edit" method="GET">
              <button class="alert button edit-btn">{% trans %}Edit{% endtrans %}</button>
              </form>
              <form action="/logout" method="POST">
              <button class="alert button logout-btn">{% trans %}Logout{% endtrans %}</button>
              </form>
            </div>
          </div>
          <div class="profile-content large-10 small-10 columns">
            <h3>{% trans %}User Information{% endtrans %}</h3>
            <table class="user-information">
            <tbody>
              <tr>
                <td>{% trans %}Language{% endtrans %}</td>
                <td>{% if user.lang == "en" %}{% trans %}English{% endtrans %}{% elif user.lang == "ja" %}{% trans %}Japanese{% endtrans %}{% else %}N/A{% endif %}</td>
              </tr>
            </tbody>
            </table>

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

            <h3>{% trans %}Proposals{% endtrans %}</h3>
{% if not sessions %}
            <p>{% trans %}No proposals have been submitted{% endtrans %}</p>
{% else %}
            <table class="session-history">
            <thead>
              <tr>
                <td>{% trans %}Title{% endtrans %}</td>
                <td>{% trans %}Conference{% endtrans %}</td>
                <td>{% trans %}Confirmed{% endtrans %}</td>
                <td>{% trans %}Edit{% endtrans %}</td>
                <td>{% trans %}Status{% endtrans %}</td>
                <td>&nbsp;</td>
              </tr>
            </thead>
            <tbody>
{% for session in sessions %}
              <tr>
                <td><span{% if session.conference.status == 'private' %} class="invalid"{% endif %}>{% if session.title %}<a href="/{{ session.conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a>{% else %}N/A{% endif %}</span></td>
                <td>{% if session.conference %}{{ session.conference.title }}{% endif %}</td>
                <td>{% if session.status != 'accepted' %}-{% elif session.confirmed %}{% trans %}confirmed{% endtrans %}{% else %}<a class="confirm-session-link" href="/{{ session.conference.full_slug }}/session/confirm">{% trans %}unconfirmed{% endtrans %}</a>{% endif %}</td>
                <td><a href="/{{ session.conference.full_slug }}/session/{{ session.id }}/edit"><span class="i-mode_edit" /></a></td>
                <td>{{ _(session.status) }}</td>
                <td><a href="/{{ session.conference.full_slug }}/session/{{ session.id }}/delete"><span class="i-delete" /></a></td>
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
