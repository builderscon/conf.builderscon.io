{% extends 'layout/conference.tpl' %}

{% block title %}{{ conference.title }} - builderscon{% endblock %}

{% block header %}
{% if conference.cover_url %}
<style type="text/css">
<!--
#heroimage {
    background: rgba(0,0,0,0) url({{ conference.cover_url }}) repeat-x center 0;
}
div.speakers div.speaker {
    margin-left: 2em;
    margin-bottom: 1em;
}
-->
</style>
{% endif %}
{% endblock %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h2>{{ conference.sub_title }}</h2>
{% if conference.dates|length == 1 %}
{% set dt = conference.dates[0]|confdate(lang=lang,timezone=conference.get('timezone')) %}
<h2>{{ dt.date() }}</h2>
{% endif %}
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
{% set description = conference.get('description') %}
{% if description %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}About The Conference{% endtrans %}</h1>
      <div class="section-content">
        <div>{{ description|markdown }}</div>
      </div>
    </div>
  </div>
{% endif %}

  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Information{% endtrans %}</h1>
      <div class="section-content">
        <h2>{% trans %}Sessions{% endtrans %}</h2>
        <div style="margin-left: 2em"><a href="/{{ conference.full_slug }}/sessions">{% trans %}Session List{% endtrans %}</a></div>

{% set dates = conference.get('dates') or [] %}{% if dates|length > 0 %}
        <h2>{% trans %}Dates{% endtrans %}</h2>
{% for date in dates %}
{% set dt = date|confdate(lang=lang, timezone=conference.get('timezone')) %}
        <div style="margin-left: 2em">{{ dt.date() }} ({{ dt.open_time() }} 〜 {{ dt.close_time() }})</div>
{% endfor %}
{% endif %}
{% set venues = conference.get('venues') or [] %}{% if venues|length > 0 %}
        <h2>{% trans %}Venue{% endtrans %}</h2>
        <div style="margin-left: 2em">
{% for venue in venues %}
          <h3>{{ venue.name }}</h3>
          <p>{{ venue.address }}</p>
          <div id="map-{{ loop.index }}" style="height: 200px"></div>
{% endfor %}
        </div>
{% endif %}
      </div>
    </div>
  </div>

{% if conference.featured_speakers|length > 0 %}
  <div class="section article speakers">
    <div class="inner">
      <h1 class="section-header">{% trans %}Guest Speakers{% endtrans %}</h1>
      <div class="section-content">
{% for speaker in conference.featured_speakers %}
        <div class="row speaker">
          <div class="large-2 small-2 columns"><img style="margin: 5px; border: 1px solid #ccc" src="{% if speaker.avatar_url %}{{ speaker.avatar_url }}{% else %}{{ url('static', filename='images/noprofile.png') }}{% endif %}" /></div>
          <div class="large-9 small-9 columns">
            <h4>{{ speaker.display_name }}</h4>
            <div>{{ speaker.description|markdown }}</div>
          </div>
        </div>
{% endfor %}
      </div>
    </div>
  </div>
{% endif %}

{% with sponsors = conference.get('sponsors') or [] %}
{% if sponsors | length > 0 %}
{% include 'sponsor_block.tpl' %}
{% endif %}
{% endwith %}

{% endblock%}

