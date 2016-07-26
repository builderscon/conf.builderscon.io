{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<style type="text/css">
<!--
    img.tier-1 {
        width: 120px;
        height: 120px;
    }
-->
</style>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Sponsors</h1>
      <div class="section-content">
        <h3 class="section-header">{{conference.title}}はこちらのスポンサーの皆様にご支援頂いています。</h3>
{% for sponsor in conference.sponsors %}
        <a href="{{ sponsor.url }}"><img class="{{ sponsor.group_name }}" src="{{ sponsor.logo_url1 }}"></a>
{% endfor %}
      </div>
    </div>
  </div>
{% endblock%}