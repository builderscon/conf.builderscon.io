{% extends 'base.tpl' %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h2>{{ conference.sub_title }}</h2>
{% endblock %}

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
