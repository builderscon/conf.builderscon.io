<!doctype html>
<html lang="ja" prefix="og:http://ogp.me/ns#">
  <head>
    <title>{% block title %}builderscon - {% trans %}Discover Something New{% endtrans %}{% endblock %}</title>
    <meta property="fb:app_id" content="1537973726511652" />
    <meta property="og:type" content="{% block ogp_type %}{% if pagetitle == 'top' %}website{% else %}article{% endif %}{% endblock %}" />
    <meta property="og:image" content="{% block og_image %}https://builderscon.io{{ url('static', filename='images/hex_logo.png') }}{% endblock %}" />
    <meta property="og:site_name" content="builderscon" />
{% for name in ["description","og:description"] %}
    <meta {% if name == 'og:description' %}property{% else %}name{% endif %}="{{ name }}" content="{% block og_description %}{% trans %}Discover Something New{% endtrans %} - {% trans %}builderscon is a festival for those who love tech!{% endtrans %}{% endblock %}" />
{% endfor %}
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <meta content="@builderscon" name="twitter:site" />
    <meta name="keywords" content="builderscon,tech,engineer,festival,お祭り" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:site" content="@builderscon" />
    <link href="{{ url('static', filename='images/favicon.ico') }}" rel="shortcut icon"/>
    <link href="{{ url('static', filename='css/style.css') }}" rel="stylesheet"/>
{% block header %}{% endblock %}
  </head>
  <body id="{% block body_id %}{% endblock %}">
    <a id="top" name="top"></a>
    <div id="wrapper">
      <header id="header">
        <div class="inner">
          <h1>
            <a href="/"><img alt="builderscon" src="{{ url('static', filename='images/logo.png') }}"/></a>
          </h1>
          <div class="btn-menu"><a href="#menu"><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></a></div><!--  / .btn-menu /  -->
        </div>
        <nav id="menu">
          <div id="gnavi">
            <ul class="menu">
              {% block menuitems %}
                <li><a href="/">{% trans %}builderscon{% endtrans %}</a></li>
                <li><a href="/dashboard">{% trans %}Dashboard{% endtrans %}</a></li>
              {% endblock %}
            </ul><!-- ul.menu -->
          </div><!-- div#gnavi -->
        </nav><!-- nav#menu -->
      </header>
{% block heroimage %}
      <div id="heroimage">
        <div class="wrapper">
          <div class="inner">
            <div class="column">
              {% block herotext %}
              {% endblock %}
            </div>
          </div>
        </div>
{% block hexlogo %}{% endblock %}
      </div>
{% endblock %}
      <div id="contents" class="index">
        {% block main %}
        {% endblock%}
      </div>
      <div id="pagetop" style="display: block;">
        <a href="#top" style="opacity: 1;"><span class="i-flight"></span></a>
      </div>
      <aside>
        <div id="footer-logo">builderscon</div>
      </aside>
      <footer id="footer">
        <div class="inner">
          <div class="contents">
            <p>{% trans %}builderscon is a festival for the technology lovers.{% endtrans %}</p>
            <p class="privacy-policy"><a href="https://docs.google.com/document/d/1mAL15VVObqIIqqKIGovnLQ4a4qQEuoACPHksq9sXbzs/edit?usp=sharing">{% trans %}Privacy Policy{% endtrans %}</a></p>
            <address>&copy; 2016 builderscon</address>
          </div>
        </div>
      </footer>
    </div>
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-84262116-1', 'auto');
      ga('send', 'pageview');
    </script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
    <script src="{{ url('static', filename='js/functions.js') }}"></script>
    <script src="{{ url('static', filename='js/jquery.cookie.js') }}"></script>
    <script src="{{ url('static', filename='js/jquery.easing.1.3.js') }}"></script>
    <script src="{{ url('static', filename='js/jquery.rotate.js') }}"></script>
    <script src="{{ url('static', filename='js/jquery.mmenu.all.min.js') }}"></script>
    <script src="{{ url('static', filename='js/foundation.min.js') }}"></script>
    <script type="text/javascript"><!--
      $(document).ready(function() {
          $(document).foundation();
      })
    --></script>
    {% block scripts %}{% endblock %}
  </body>
</html>
