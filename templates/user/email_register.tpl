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
      <h1 class="section-header">{% trans %}Register Your Email{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <p class="large-12 columns">{% trans %}In order to proceed with your submission, you must first register a valid email address. This is required so we know how to contact you regarding your submission, and to notify you of any important updates.{% endtrans %}</p>
        </div>
        <form id="registration-form" method="POST" action="/user/email/register">
          <div class="row">
            <div class="large-4 columns">
              <input type="text" name="email"{% if user.email %} value="{{ user.email }}"{% endif %}>
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
