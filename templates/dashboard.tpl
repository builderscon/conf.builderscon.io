{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
div.profile {
  padding: 5px;
}
div.profile img {
  padding: 2px;
  border: 1px solid #ccc;
}
div.profile p.name {
  text-align: center;
}
span.auth_via {
  border: 1px solid #0a0;
  background-color: #cfc;
  font-weight: bold;
  font-size: 0.6em;
  color: #0a0;
  padding: 0.2em;
}
div.profile-content {
  padding-left: 1em;
}
div.conference-history {
  padding-left: 2em;
}

.invalid {
  color: #ccc;
}

-->
</style>
{% endblock %}

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
              <img src="{{ user.avatar_url }}">
              <p class="name">{{ user.nickname }} <span class="auth_via">{{ user.auth_via }}</span></p>
              <form action="/logout" method="POST">
              <button class="alert button">{% trans %}Logout{% endtrans %}</button>
              </form>
            </div>
          </div>
          <div class="profile-content large-10 small-10 columns">
{% if conferences %}
            <h3>{% trans %}Organizer{% endtrans %}</h3>
            <div class="conference-history">
{% for conference in conferences %}
              <div class="row">
                <div class="large-3 columns"><a href="/{{ conference.full_slug }}">{{ conference.title }}</a></div>
              </div>
{% endfor %}
            </div>
{% endif %}

            <h3>Proposals</h3>
{% if not sessions %}
            <p>{% trans %}No proposals have been submitted{% endtrans %}</p>
{% else %}
            <table class="session-history">
            <thead>
              <tr>
                <td>{% trans %}Conference{% endtrans %}</td>
                <td>{% trans %}Title{% endtrans %}</td>
                <td>&nbsp;</td>
                <td>{% trans %}Status{% endtrans %}</td>
                <td>&nbsp;</td>
              </tr>
            </thead>
            <tbody>
{% for session in sessions %}
              <tr>
                <td>{% if session.conference %}{{ session.conference.title }}{% endif %}</td>
                <td><span{% if session.conference.status == 'private' %} class="invalid"{% endif %}>{% if session.title %}<a href="/{{ session.conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a>{% else %}N/A{% endif %}</span></td>
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
