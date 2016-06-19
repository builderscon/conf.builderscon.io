<div id="heroimage">
  <div class="wrapper">
    <div class="inner">
      <div class="column">
        {% if conferenct %}
        <h1>{{ conference.title }}</h1>
        <h2>{{ conference.sub_title }}</h2>
        {% else %}
        <h1>Builders Conference</h1>
        <h2>builderscon is a festival for the technology lovers.</h2>
        {% endif %}
      </div>
    </div>
  </div>
</div>
