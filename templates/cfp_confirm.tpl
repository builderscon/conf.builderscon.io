{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
.notice-small {
  font-size: 80% !important;
  color: #888 !important;
}

.centered {
    text-align: center !important;
    margin: 0 auto 0 auto !important;
    float: none !important;
}

.edit-button {
    margin: 1em auto 1em auto !important;
    float: none !important;
}

.submission-verify .row {
    margin-bottom: 1em;
}

.submission-verify .value {
    border-bottom: 1px solid #ccc;
}
-->
</style>
{% endblock %}

{% block main %}
{% set leftcol = 4 %}
{% set rightcol = 12 - leftcol %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Submission Details{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-12 columns">
            <p class="centered notice-small">{% trans %}Please review your submission details below. If you have corrections to make, click the button below to edit your submission{% endtrans %}</p>
          </div>
        </div>

        <div class="row">
          <div class="large-3 columns edit-button">
            <a href="/{{ conference.full_slug }}/cfp?key={{ submission_key }}" id="edit-button" type="submit" class="expanded button">{% trans %}Edit your proposal{% endtrans %}</a>
            </form>
          </div>
        </div>

        <div class="submission-verify">
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Title (English){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.title %}{{ session.title }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Title (Japanese){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.get('title#ja') }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Duration{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session_type.name }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Abstract (English){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.abstract %}{{ session.abstract | markdown }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Abstract (Japanese){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.get('abstract#ja') %}{{ session.get('abstract#ja') | markdown }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Material Level{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.material_level|audlevelname) }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Spoken Language{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.spoken_language|langname) }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Slide Language{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.slide_language|langname) }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Comments{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.memo %}{{ session.memo }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Photo Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.photo_release|permname) }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Recording Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.recording_release|permname) }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Materials Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ _(session.materials_release|permname) }}</div>
        </div>
        </div>
        <div class="row">
          <div class="large-12 columns">
            <form action="/{{ conference.full_slug }}/cfp/commit" method="POST">
              <input type="hidden" name="key" value="{{ submission_key }}">
            <button id="submit-button" type="submit" class="expanded button">{% trans %}Submit your proposal{% endtrans %}</button>
            </form>
          </div>
        </div>
      </div>
    <div>
  </div>
</main>
{% endblock %}
