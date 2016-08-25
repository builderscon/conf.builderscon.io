{% extends 'layout/base.tpl' %}
{% block title %}{% trans %}Mr. B{% endtrans %} - builderscon{% endblock %}
{% block og_description %}{% trans %}Meet Mr. B (Mr. Beacon)!{% endtrans %}{% endblock %}
{% block og_image %}https://builderscon.io{{ url('static', filename='images/mrbeacon-004.png') }}{% endblock %}
{% block body_id %}beacon{% endblock %}
{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="http://blog.builderscon.io">{% trans %}BLOG{% endtrans %}</a></li>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Meet Mr. B (Mr. Beacon)!{% endtrans %}</h1>
      <div class="section-content">
        {% trans %}
        <p>Mr. B is our jolly mascot beaver. He likes to build stuff, just like us</p>
        <p>Please feel free to use Mr B. for promoting your own builderscon or to create new swags with it!</p>
        {% endtrans %}
      </div>
    </div>
  </div>
  <div class="section article" id="beacon-gallery">
    <div class="inner">
      <div class="section-content no-header">
{% for i in range(1,10) %}
{% if i % 3 == 1 %}
        <div class="row">
{% endif %}
          <div class="large-4 columns gallery-slot">
            <a href="{{ url('static', filename='images/mrbeacon-%03d.png' % i) }}"><img src="{{ url('static', filename='images/mrbeacon-%03d.png' % i) }}"></a>
            <div class="title">mrbeacon-{{ '%03d' % i }}.png</div>
          </div>
{% if i % 3 == 0 or loop.last %}
        </div>
{% endif %}
{% endfor %}
      </div>
    </div>
  </div>
  <div class="section article" id="tou">
    <div class="inner">
      <h1 class="section-header">{% trans %}Terms Of Use{% endtrans %}</h1>
      <div class="section-content">
        {% trans %}
        <ul>
            <li>Permission is hereby granted to use the Mr. Beacon character, in accordance with <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC-BY-NC 4.0 License</a></li>
            <li>Mr. Beacon was designed by <a href="https://twitter.com/yassang0928">yassang</a></li>
            <li>Attribution to the creator ("by yassang") is recommended but not required</li>
            <li>Mr. Beacon is &copy; endeworks and &copy; <a href="https://twitter.com/yassang0928">yassang</a></li>
        </ul>
        {% endtrans %}
      </div>
    </div>
  </div>
</main>
{% endblock %}
