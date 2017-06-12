{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h3>{{ conference.sub_title }}</h3>
<h3>{% if conference.dates|length == 1 %}{{ conference.dates[0].date }}{% endif %}</h3>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <div class="section-content no-header">
        <p>{% trans %}Thank your for your submission!{% endtrans %} <a href="/{{ conference.full_slug }}/session/{{ session.id }}">{% trans %}Your submission can be viewd here{% endtrans %}</a></p>
      </div>
    </div>
  </div>
{% if conference.get('cfp_post_submit_instructions') %}
  <div class="section article">
    <div class="inner">
      <div class="section-content no-header">
        {{ conference.cfp_post_submit_instructions | markdown }}
      </div>
    </div>
  </div>
{% endif %}
</main>
{% endblock %}
