{% extends 'layout/base.tpl' %}
{% block title %}{% trans %}Error{% endtrans %} - builderscon{% endblock %}
{% block body_id %}error{% endblock %}
{% block contents_id %}error{% endblock %}
{% block heroimage %}{% endblock %}
{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="/dashboard">{% trans %}Dashboard{% endtrans %}</a></li>
<li><a href="http://blog.builderscon.io">{% trans %}BLOG{% endtrans %}</a></li>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}There was an error{% endtrans %}</h1>
      <div class="section-content">
        {% if error | is_oauth_error %}{% trans %}We received an error from an external site.{% endtrans %}{% else %}There was an error.{% endif %} {% trans %}Please try again in a few minutes.{% endtrans %}
      </div>
    </div>
  </div>
</main>
{% endblock %}
