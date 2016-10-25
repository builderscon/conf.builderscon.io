{% extends 'layout/conference.tpl' %}

{% block body_id %}session{% endblock %}
{% block title %}{% trans %}Confirm your session{% endtrans %} - {{ conference.title }}{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<div id="fb-root"></div>
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Session confirmed{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-12 small-12 columns">
            <p>{{ _("Thank you for taking the time to confirm your session. Your session has been confirmed as below. We hope to see you soon at %(title)s.", title=conference.title) }}</p>
            <table>
            <thead>
              <tr>
                <td>{% trans %}Title{% endtrans %}</td>
                <td>{% trans %}Conference{% endtrans %}</td>
                <td>{% trans %}Starts On{% endtrans %}</td>
                <td>{% trans %}Room{% endtrans %}</td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a></td>
                <td><a href="/{{ conference.full_slug }}">{{ conference.title }}</a></td>
                <td>{% if session.starts_on %}{{ session.starts_on | dateobj | datefmt(locale=lang,tzinfo=conference.timezone) }}{% endif %}</td>
                <td>{% if session.room %}{{ session.room.name }}{% if session.room.venue %} {{ session.room.venue.name }}{% endif %}{% endif %}</td>
              </tr>
            </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock%}
