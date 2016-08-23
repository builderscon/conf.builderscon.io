{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
{% include 'session/form_header.tpl' %}
{% endblock %}

{% block scripts %}
{% include 'session/form_scripts.tpl' %}
{% endblock %}

{% block main %}
<main>
{% if not errors %}
{% block cfp_lead_text %}
  {% if 'cfp_lead_text' in conference %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Call For Papers{% endtrans %}</h1>
      <div class="section-content">
        {{ conference.cfp_lead_text | markdown }}
      </div><!-- section-content -->
    </div><!-- inner -->
  </div><!-- section article -->
  {% endif %}
{% endblock %}
{% block cfp_pre_submit_instructions %}
  {% if 'cfp_pre_submit_instructions' in conference %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Submission Instructions{% endtrans %}</h1>
      <div class="section-content">
        {{ conference.cfp_pre_submit_instructions | markdown }}
      </div><!-- section-content -->
    </div><!-- inner -->
  </div><!-- section article -->
  {% endif %}
{% endblock %}
{% endif %}
{% with action='/%s/cfp/input' % full_slug %}
{% include "session/form.tpl" %}
{% endwith %}
</main>
{% endblock%}


