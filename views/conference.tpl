{% extends 'layout/conference.tpl' %}

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
      draggable: false,
      scrollwheel: false,
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
      <h1 class="section-header">Dates</h1>
      <div class="section-content">
        <h2>Dates</h2>
{% for date in conference.dates %}
        <div style="margin-left: 2em">{{ date.date }}</div>
{% endfor %}
        <h2>Venue</h2>
        <div style="margin-left: 2em">
{% for venue in conference.venues %}
          <h3>{{ venue.name }}</h3>
          <p>{{ venue.address }}</p>
          <div id="map-{{ loop.index }}" style="height: 200px"></div>
{% endfor %}
        </div>
      </div>
    </div>
  </div>

{% if conference.featured_speakers|length > 0 %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Guest Speakers</h1>
      <div class="section-content">
{% for speaker in conference.featured_speakers %}
        <div class="row" style="margin-left: 2em">
<div class="large-2 columns"><img style="width: 120px; height: 120px; border: 1px solid #ccc" src="{% if speaker.avatar_url %}{{ speaker.avatar_url }}{% else %}{{ url('statics', filename='images/noprofile.png') }}{% endif %}" /></div>
<div class="large-10 columns">
    <h4>{{ speaker.display_name }}</h4>
    <div>{{ speaker.description|markdown }}</div>
</div>
        </div>
{% endfor %}
      </div>
    </div>
  </div>
{% endif %}

{% endblock%}
