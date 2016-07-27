{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Sessions{% endtrans %}</h1>
      <div class="section-content">
        <div class="row" style="margin-left: 2em">
          <div class="large-2 columns">
            <img style="width: 120px; height: 120px; border: 1px solid #ccc" src="https://conf.builderscon.io/assets/images/noprofile.png"/>
          </div>
          <div class="large-10 columns">
            <div class="row" style="margin-left: 2em">
               <h4>Session title, by speaker name</h4>
            </div>
            <div class="row" style="margin-left: 2em">
               <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,
               sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
               Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
               ut aliquip ex ea commodo consequat.</p>
            </div>
          </div>
        </div>
        <div class="row" style="margin-top: 2em">
          <a class="expanded button" href="session/add">{% trans %}Submit your proposal{% endtrans %}</a>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock%}
