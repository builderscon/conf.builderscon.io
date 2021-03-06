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
      <h1 class="section-header">{% trans %}Confirm your session{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-12 small-12 columns">
{% if not sessions %}
            <p>{% trans %}There are no sessions that needs confirming{% endtrans %}</[
{% else %}
            <p>{% trans %}Below sessions have been accepted, but you have not yet confirmed that you can attend. Please confirm that you are in fact attending the conference, and that you are okay with the presented schedule for the accepted talk(s) below. If you do not confirm, your session <strong>may be canceled</strong> by the organizers. If you have schedulding conflicts, please contact the organizers immediately.{% endtrans %}</p>
            <table>
            <thead>
              <tr>
                <td>&nbsp;</td>
                <td>{% trans %}Title{% endtrans %}</td>
                <td>{% trans %}Conference{% endtrans %}</td>
                <td>{% trans %}Starts On{% endtrans %}</td>
                <td>{% trans %}Room{% endtrans %}</td>
              </tr>
            </thead>
            <tbody>
{% for session in sessions %}
              <tr>
                <td><a class="confirm-button success button" data-title="{{ session.title|urlencode }}" data-id="{{ session.id }}">{% trans %}Confirm{% endtrans %}</a></td>
                <td><a href="/{{ conference.full_slug }}/session/{{ session.id }}">{{ session.title }}</a></td>
                <td><a href="/{{ conference.full_slug }}">{{ conference.title }}</a></td>
                <td>{% if session.starts_on %}{{ session.starts_on | dateobj | datefmt(locale=lang,tzinfo=conference.timezone) }}{% endif %}</td>
                <td>{% if session.room %}{{ session.room.name }}{% if session.room.venue %} {{ session.room.venue.name }}{% endif %}{% endif %}</td>
              </tr>
{% endfor %}
            </tbody>
            </table>
{% endif %}
          </div>
        </div>
      </div>
    </div>
  </div>
</main>

{% include 'session/reconfirm-modal.tpl' %}
{% endblock%}

{% block scripts %}
{% include 'session/reconfirm-modal-js.tpl' %}
{% endblock %}
