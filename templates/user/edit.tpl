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
{% if next_url %}
          <input type="hidden" name=".next" value="{{ next_url | e }}" />
{% endif %}
          <div class="row">
            <div class="large-{{ left }} columns">
              <label>{% trans %}Language{% endtrans %}</label>
              <div class="label-sub">{% trans %}The language that this web site will be displayed in{% endtrans %}</div>
            </div>
            <div class="large-{{ right }} columns">
              <select id="select-lang" name="lang">
                <option value="en">{% trans %}English{% endtrans %}</option>
                <option value="ja">{% trans %}Japanese{% endtrans %}</option>
              </select>
            </div>
          </div>
          <div class="row button-row">
            <div class="large-4 columns">&nbsp;</div>
            <div class="large-4 columns">
              <button id="submit-button" type="submit" class="expanded button">{% trans %}Update{% endtrans %}</button>
            </div>
            <div class="large-4 columns">&nbsp;</div>
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
$(document).ready(function() {
  $("#select-lang").val("{{ user.lang }}");
})
-->
</script>
{% endblock %}
