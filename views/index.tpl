{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
  #contents.index { padding: 180px 0 0 0 }
-->
</style>
{% endblock %}

{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="http://blog.builderscon.io">{% trans %}BLOG{% endtrans %}</a></li>
{% endblock %}

{% block hexlogo %}
<div id="hexlogo">
<div class="base"><img src="./assets/images/hex_base.png" /></div><!--  / .base /  -->
<div class="logo"><img src="./assets/images/hex_logo.png" /></div><!--  / .logo /  -->
</div><!--  / #hexlogo /  -->
{% endblock %}

{% block herotext %}
<img src="{{ url('statics', filename='images/builderscon-text.png') }}" width="350">
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Welcome To builderscon{% endtrans %}</h1>
      <div class="section-content">
        {% trans %}
        <strong>Join builderscon and discover something new! builderscon is a festival (お祭り）for anybody who loves tech.</strong>
        <p>builderscon is a tech-agnostic, polyglot conference. The only thing we ask of you is that you come and discuss about things that gets engineers -- the builders of modern age -- excited.</p>
        <p>Show us your crazy hacks; Get down to the nitty-gritty details about your favorite language; Tell us the problems that you encountered, and how you solved them; Teach us about future technologies</p>
        <p>Please join us and share your passion about tech: We would love to hear your stories!</p>
        {% endtrans %}

      </div>
    </div>
  </div>

  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Upcoming Conferences{% endtrans %}</h1>
      <div class="section-content">
        <table>
          <tbody>
            {% for conference in conferences %}
            <tr>
              <td>
                <a href="{% if conference.series %}{{ conference.series.slug }}/{% endif %}{{ conference.slug }}">{{ conference.title }}</a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</main>
{% endblock%}
