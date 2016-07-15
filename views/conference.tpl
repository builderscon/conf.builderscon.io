{% extends 'base.tpl' %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h2>{{ conference.sub_title }}</h2>
<h2>{% if conference.dates|length == 1 %}{{ conference.dates[0].date }}{% endif %}</h2>
{% endblock %}

{% block scripts %}
{% if conference.venues|length > 0 %}
<script type="text/javascript">
<!--
var map;
function initMap() {
{% for venue in conference.venues %}
  (function() {
    var latlng = {lat: {{ venue.latitude }}, lng: {{ venue.longitude }}};
    map = new google.maps.Map(document.getElementById('map-{{ loop.index }}'), {
      center: latlng,
      zoom: 14
    });
    var marker = new google.maps.Marker({
      position: latlng,
      map: map,
      title: "{{ venue.name }}",
    });
  })()
{% endfor %}
}
-->
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key={{ googlemap_api_key }}&callback=initMap"></script>
{% endif %}
{% endblock %}

{% block main %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Information</h1>
      <div class="section-content">
        <h2>Dates</h2>
{% for date in conference.dates %}
        <p>{{ date.date }}</p>
{% endfor %}
        <h2>Venue</h2>
        <div style="margin-left: 2em">
{% for venue in conference.venues %}
          <h3>{{ venue.name }}</h3>
          <p>{{ venue.address }}</p>
          <div id="map-{{ loop.index }}" style="height: 200px"></div>
{% endfor %}
        </div>
        <a class="expanded button" href="/{{ conference.series.slug }}/{{ conference.slug }}/sessions">sessions</a>
      </div>
    </div>
  </div>
{% endblock%}
