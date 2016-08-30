{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
#registration-form {
  margin-bottom: 5em;
}
-->
</style>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Confirm Email Address{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <p class="large-12 columns">{% trans %}Thank you! Your email has been registered.{% endtrans %}</p>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock %}
