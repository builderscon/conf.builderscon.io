{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block body_id %}schedule{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{ _("Sessions for %(date)s", date=date) }}</h1>
      <div class="section-content timetable">
        <div class="dates">| {% for cdt in conference.get('dates') %}
        {% set cds = (cdt.open | dateobj).strftime('%Y-%m-%d') %}
        <a href="/{{ conference.get('full_slug') }}/timetable?date={{ cds }}">{{ cds }}</a>{% if not loop.last %} | {% endif %}
        {% endfor %} |</div>
        {{ table }}
      </div>
    </div>
  </div>
</main>
{% endblock %}
