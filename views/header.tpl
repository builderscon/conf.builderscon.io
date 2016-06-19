<header id="header">
  <div class="inner">
    <h1>
      <a href="/">
        <img alt="builderscon" src="{{ url('statics', filename='images/logo.png') }}"/>
      </a>
    </h1>
  </div>
  <nav id="menu">
    <div id="gnavi">
      <ul class="menu">
        {% if not login %}
        <li><a href="login">LOGIN</a></li>
        {% endif %}
      </ul>
    </div>
  </nav>
</header>
