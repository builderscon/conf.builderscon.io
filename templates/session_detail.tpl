{% extends 'layout/base.tpl' %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{session.title}}</h1>
      <div class="section-content">

        <div class="row">
          <div class="small-6 large-2 columns">
            <img style="width: 120px; height: 120px; border: 1px solid #ccc" src="{% if session.speaker.avatar_url %}{{ session.speaker.avatar_url }}{% else %}{{ url('static', filename='images/noprofile.png') }}{% endif %}" />
            <div class="text-center"><a  href="." target="_blank">{{session.speaker.nickname}}</a></div>
          </div>
        </div>

        <div class="row">
          <div class="small-12 columns">
            <p>
              {{session.abstract}}
            </p>
          </div>
        </div>

        <div class="row">
          <table>
            <tr>
              <td>Material Level</td>
              <td>{{session.material_level}}</td>
            </tr>
            <tr>
              <td>Starts On</td>
              <td>{{session.starts_on}}</td>
            </tr>
            <tr>
              <td>Duration</td>
              <td>{{session.session_type.name}}</td>
            </tr>
            <tr>
              <td>Spoken Language</td>
              <td>{{session.spoken_language}}</td>
            </tr>
            <tr>
              <td>Slide Language</td>
              <td>{{session.slide_language}}</td>
            </tr>
            <tr>
              <td>May we take your photo?</td>
              <td>{{session.photo_permission}}</td>
            </tr>
            <tr>
              <td>May we record your session?</td>
              <td>{{session.video_permission}}</td>
            </tr>
          </table>
        </div>

      </div>
    </div>
  </div>
</main>
{% endblock%}
