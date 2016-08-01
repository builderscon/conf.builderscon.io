{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
  #contents.index { padding: 180px 0 0 0 }
  #conferences .conference-name { font-size: 1.5em; vertical-align: middle }
  #get-involved .inner .section-content div.row {
    margin: 1em 0 0 1em;
  }
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

  <div class="section article" id="conferences">
    <div class="inner">
      <h1 class="section-header">{% trans %}Upcoming Conferences{% endtrans %}</h1>
      <div class="section-content">
        {% for conference in conferences %}
        <div class="row">
          <div class="large-1 column">
            <img src="{{ url('statics', filename='images/hex_logo.png') }}" style="width: 32px; height: 32px">
          </div>
          <div class="large-11 column">
            <a class="conference-name" href="{% if conference.series %}{{ conference.series.slug }}/{% endif %}{{ conference.slug }}">{{ conference.title }}</a> ({{ conference.dates[0] | dateobj(lang=lang) }})
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>

  <div class="section article" id="get-involved">
    <div class="inner">
      <h1 class="section-header">{% trans %}Get Involved!{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-1 column">
            <img src="https://a.slack-edge.com/0180/img/icons/app-256.png" style="width: 64px; height: 64px;">
          </div>
          <div class="large-11 column">
            <p>{% trans %}<b>Slack: </b> We have <a href="https://builderscon.slack.com">a Slack team</a>, and <a href="https://slack-invite-dot-builderscon-1248.appspot.com/">you can invite yourself</a>. Come and share your knowledge of conference organization, or ask to get started on your own builderscon!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 column">
            <img src="https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png" style="width: 64px; height: 64px;">
          </div>
          <div class="large-11 column">
            <p>{% trans %}<b>Github:</b> Explore our many opensource projects on <a href="https://github.com/builderscon">Github</a>, including our "<a href="https://github.com/builderscon/builderscon">spec</a>", our <a href="https://github.com/builderscon/octav">API server</a>, and <a href="https://github.com/builderscon/builderscon.io">this site</a>. We'd love for your to send us pull requests!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 column">
            <img src="https://www.facebookbrand.com/img/fb-art.jpg" style="width: 64px; height: 64px;">
          </div>
          <div class="large-11 column">
            <p>{% trans %}<b>Facebook:</b> Peruse our <a href="https://www.facebook.com/builderscon">Facebook page</a> to find various events that we host for people interested in builderscon like our now famous BBQ [<a href="https://www.facebook.com/events/803942576374123/">1</a>][<a href="https://www.facebook.com/events/1091601347586795/">2</a>]</a>{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 column">
            <img src="https://g.twimg.com/Twitter_logo_blue.png" style="width: 64px; height: 52px;">
          </div>
          <div class="large-11 column">
            <p>{% trans %}<b>Twitter:</b> Follow us on <a href="https://twitter.com/builderscon">Twitter</a>, and get the latest updates!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 column">
            <img src="{{ url('statics', filename='images/mrbeacon-001.png') }}" style="width: 64px; height: 64px;">
          </div>
          <div class="large-11 column">
            <p>{% trans %}<b>Share:</b> Read our <a href="http://blog.builderscon.io">blog</a>, post on your favorite sites, and perhaps if you are feeling like it, you can use <a href="/beacon">our Mr. B images</a> to spice up your online conversations.{% endtrans %}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock%}
