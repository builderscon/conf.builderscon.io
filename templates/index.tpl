{% extends 'layout/base.tpl' %}

{% block body_id %}top{% endblock %}

{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="/dashboard"><span class="i-user"></span></a></li>
<li><a href="http://blog.builderscon.io">{% trans %}BLOG{% endtrans %}</a></li>
{% endblock %}

{% block hexlogo %}
<div id="hexlogo">
<div class="base"><img src="/static/images/hex_base.png" /></div><!--  / .base /  -->
<div class="logo"><img src="/static/images/hex_logo.png" /></div><!--  / .logo /  -->
</div><!--  / #hexlogo /  -->
{% endblock %}

{% block herotext %}
<img src="{{ url('static', filename='images/builderscon-text.png') }}" width="350">
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

  <div class="section article conferences">
    <div class="inner">
      <h1 class="section-header">{% trans %}Upcoming Conferences{% endtrans %}</h1>
      <div class="section-content">
        {% for conference in conferences %}
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="{{ url('static', filename='images/hex_logo.png') }}">
          </div>
          <div class="large-11 small-11 column conference-name">
            <a href="{% if conference.series %}{{ conference.series.slug }}/{% endif %}{{ conference.slug }}">{{ conference.title }}</a> ({{ conference.dates[0] | dateobj(lang=lang) }})
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>

  <div class="section article get-involved">
    <div class="inner">
      <h1 class="section-header">{% trans %}Get Involved!{% endtrans %}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="https://a.slack-edge.com/0180/img/icons/app-256.png">
          </div>
          <div class="large-11 small-11 column get-involved-description">
            <p>{% trans %}<b>Slack: </b> We have <a href="https://builderscon.slack.com">a Slack team</a>, and <a href="https://slack-invite-dot-builderscon-1248.appspot.com/">you can invite yourself</a>. Come and share your knowledge of conference organization, or ask to get started on your own builderscon!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="/static/images/github-120px.png">
          </div>
          <div class="large-11 small-11 column get-involved-description">
            <p>{% trans %}<b>Github:</b> Explore our many opensource projects on <a href="https://github.com/builderscon">Github</a>, including our "<a href="https://github.com/builderscon/builderscon">spec</a>", our <a href="https://github.com/builderscon/octav">API server</a>, and <a href="https://github.com/builderscon/builderscon.io">this site</a>. We'd love for your to send us pull requests!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="/static/images/facebook-120px.jpg">
          </div>
          <div class="large-11 small-11 column get-involved-description">
            <p>{% trans %}<b>Facebook:</b> Peruse our <a href="https://www.facebook.com/builderscon">Facebook page</a> to find various events that we host for people interested in builderscon like our now famous BBQ [<a href="https://www.facebook.com/events/803942576374123/">1</a>][<a href="https://www.facebook.com/events/1091601347586795/">2</a>]</a>{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="/static/images/twitter-120px.png">
          </div>
          <div class="large-11 small-11 column get-involved-description">
            <p>{% trans %}<b>Twitter:</b> Follow us on <a href="https://twitter.com/builderscon">Twitter</a>, and get the latest updates!{% endtrans %}</p>
          </div>
        </div>
        <div class="row">
          <div class="large-1 small-1 column">
            <img src="{{ url('static', filename='images/mrbeacon-001.png') }}">
          </div>
          <div class="large-11 small-11 column get-involved-description">
            <p>{% trans %}<b>Share:</b> Read our <a href="http://blog.builderscon.io">blog</a>, post on your favorite sites, and perhaps if you are feeling like it, you can use <a href="/beacon">our Mr. B images</a> to spice up your online conversations.{% endtrans %}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  {% set technical_sponsors = [
      dict(
          name = 'ClubT',
          group_name = 'tier-1',
          url = 'https://clubt.jp',
          logo_url1 = 'https://storage.googleapis.com/media-builderscon-1248/system/clubT-600x600.png'
      ),
      dict(
          name = 'Google Cloud Platform',
          group_name = 'tier-1',
          url = 'https://cloud.google.com/',
          logo_url1 = 'https://storage.googleapis.com/media-builderscon-1248/system/gcp-600x600.png'
      ),
      dict(
          name = 'GitHub',
          group_name = 'tier-1',
          url = 'https://github.com/',
          logo_url1 = 'https://storage.googleapis.com/media-builderscon-1248/system/github-600x600.png'
      ),
      dict(
          name = 'Mackerel',
          group_name = 'tier-1',
          url = 'https://mackerel.io',
          logo_url1 = 'https://storage.googleapis.com/media-builderscon-1248/system/mackerel-600x600.png'
      )
  ] %}
  {% with sponsors = technical_sponsors, sponsor_header='Technical Sponsors' %}
  {% include 'sponsor_block.tpl' %}
  {% endwith %}

</main>
{% endblock %}
