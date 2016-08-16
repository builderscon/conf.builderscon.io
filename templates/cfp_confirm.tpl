{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
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
<main>
{% set leftcol = 3 %}
{% set rightcol = 12 - leftcol %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Submission Details{% endtrans %}</h1>
      <div class="section-content">
        <div class="submission-verify">
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Title (English){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.title %}{{ session.title }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Title (Japanese){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.get('title#ja') }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Session Type{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.get('session_type').name }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Abstract (English){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{% if session.abstract %}{{ session.abstract }}{% else %}-{% endif %}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Abstract (Japanese){% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.get('abstract#ja') }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Expected audience level{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.material_level }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Spoken Language{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.spoken_language }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Slide Language{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.slide_language }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Comments{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.memo }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Photo Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.photo_permission }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Recording Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.video_permission }}</div>
        </div>
        <div class="row">
          <div class="large-{{ leftcol }} columns">{% trans %}Materials Release{% endtrans %}</div>
          <div class="large-{{ rightcol }} columns value">{{ session.materials_release }}</div>
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
