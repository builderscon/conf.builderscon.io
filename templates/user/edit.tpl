{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
{% set left = 3 %}
{% set right = 12 - left %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Edit User Information{% endtrans %}</h1>
      <div class="section-content">
        <form class="user-form" action="/user/update" method="POST">
          <div class="row">
            <div class="large-{{ left }} columns"><label>{% trans %}Language{% endtrans %}</label></div>
            <div class="large-{{ right }} columns">
              <select id="#select-lang" name="lang">
                <option value="en">{% trans %}English{% endtrans %}</option>
                <option value="ja">{% trans %}Japanese{% endtrans %}</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div class="large-12 columns">
              <button id="submit-button" type="submit" class="expanded button">{% trans %}Update{% endtrans %}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
{% endblock %}

{% block scripts %}
<script>
<!--
$(function() {
  $("#select-lang").val("{{ user.lang }}");
})
-->
</script>
{% endblock %}
