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
          <p class="large-12 columns">{% trans %}To proceed with your registration, please enter your confirmation key below{% endtrans %}</p>
        </div>
        <form id="registration-form" method="POST" action="/user/email/confirm">
          <div class="row">
            <div class="large-4 columns">
              <input type="text" name="confirmation_key"{% if confirmation_key %} value="{{ confirmation_key }}"{% endif %}>
            </div>
          </div>
          <div>
            <div class="large-4 columns">
              <button id="submit-button" type="submit" class="expanded button"><span class="i-paper-plane"></span> {% trans %}Register this email address{% endtrans %}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
{% endblock %}
