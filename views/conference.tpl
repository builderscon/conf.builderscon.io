{% extends 'base.tpl' %}

{% set eyecatch=True %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">news</h1>
      <div class="section-content">

      </div>
    </div>
  </div>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Information</h1>
      <div class="section-content">
        <h2>Date</h2>
        <p></p>
        <h2>Place</h2>
        <p></p>
        <a class="expanded button" href="/{{ conference.series.slug }}/{{ conference.slug }}/sessions">sessions</a>
      </div>
    </div>
  </div>
</main>
{% endblock%}
