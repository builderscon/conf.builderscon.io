{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
.section-content div.login-row {
  margin: 1em;
}

.login-icon img{
  padding: 0;
  width: 40px;
  height: 40px;
}

.login-link {
  font-weight: bold;
  font-size: 2em;
}
-->
</style>
{% endblock %}

{% block main %}
<main>
{% if error %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Error{% endtrans %}</h1>
      <div class="section-content">{{ _(error) }}</div>
    </div>
  </div>
{% endif %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Login{% endtrans %}</h1>
      <div class="section-content">
{% for href, name, image in [ ('/login/github', 'GitHub', '/static/images/github-120px.png'), ('/login/facebook', 'Facebook','/static/images/facebook-120px.jpg'), ( '/login/twitter', 'Twitter','/static/images/twitter-120px.png') ] %}
        <div class="login-row row">
          <div class="login-icon large-1 columns">
            <img src="{{ image }}">
          </div>
          <div class="login-link large-11 columns">
            <a href="{{ href }}{% if next_url %}?.next={{ next_url | urlencode }}{% endif %}">{% trans %}Login with {{ name }}{% endtrans %}</a>
          </div>
        </div>
{% endfor %}
      </div>
    </div>
  </div>
</main>
{% endblock%}
