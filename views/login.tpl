{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
img.login-icon {
  padding: 0;
  width: 40px;
  height: 40px;
}
-->
</style>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Login{% endtrans %}</h1>
      <div class="section-content">
        <h2><img src="/assets/images/GitHub-Mark-120px-plus.png" class="login-icon"> <a class="post-link" href="/login/github">{% trans %}Login with Github{% endtrans %}</a></h2>
      </div>
    </div>
  </div>
</main>
{% endblock%}
