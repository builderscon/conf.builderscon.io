{% extends 'base.tpl' %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <div class="section-content no-header">
        <form action="">
          <div class="row">
            <div class="large-12 columns">
              <label>
                Username
                <input type="text">
              </label>
            </div>
          </div>
          <div class="row">
            <div class="large-12 columns">
              <label>
                Password
                <input type="password">
              </label>
            </div>
          </div>
          <div class="row">
            <a class="expanded button" href="">login</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
{% endblock%}
