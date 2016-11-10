{% extends 'layout/conference.tpl' %}

{% block body_id %}session{% endblock %}
{% block title %}{{ session.title }} - {{ session.conference.title }}{% endblock %}
{% block header %}
<link rel="canonical" href="/{{ conference.full_slug }}/session/{{ session.id }}" />
{% endblock %}
{% block og_image %}{{ session.speaker.avatar_url or url('static', filename='images/noprofile.png') }}{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<div id="fb-root"></div>
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{session.title}}<span class="status-{{session.status}}">{{ _(session.status) }}</span></h1>
      <div class="section-content">
        <div class="row">
          <div class="text-center large-2 small-4 columns">
            <img style="width: 120px; height: auto; border: 1px solid #ccc" src="{% if session.speaker.avatar_url %}{{ session.speaker.avatar_url }}{% else %}{{ url('static', filename='images/noprofile.png') }}{% endif %}" />
            <div class="text-center"><a href="/user/{{ session.speaker.id }}" target="_blank">{{session.speaker.nickname}}</a><br />
        {% if user and (user.is_admin or user.id == session.speaker.id) %}<a id="session-edit-btn" href="/{{ conference.full_slug }}/session/{{ session.id }}/edit">{% trans %}Edit{% endtrans %}</a>{% endif %}
</div>
            <div class="social-button">
              <a href="http://b.hatena.ne.jp/entry/" class="hatena-bookmark-button" data-hatena-bookmark-layout="vertical-balloon" data-hatena-bookmark-lang="{{ lang }}" title="このエントリーをはてなブックマークに追加"><img src="https://b.st-hatena.com/images/entry-button/button-only@2x.png" alt="このエントリーをはてなブックマークに追加" width="20" height="20" style="border: none;" /></a><script type="text/javascript" src="https://b.st-hatena.com/js/bookmark_button.js" charset="utf-8" async="async"></script>
            </div>
            <div class="social-button">
              <div class="g-plusone" data-size="tall"  data-href="{{url}}"></div>
            </div>
            <div class="social-button">
              <div class="fb-like" data-href="/{{ conference.full_slug }}/session/{{ session.id }}" data-layout="box_count" data-action="like" data-size="large" data-show-faces="false" data-share="false"></div>
            </div>
            <div class="social-button">
              <a href="https://twitter.com/share" class="twitter-share-button" data-size="large">Tweet</a>
            </div>

            <!-- add new buttons here e.g. edit session details button -->

          </div><!-- columns -->
          <div class="large-10 small-8 columns">
            <div class="abstract">
              <h5>{% trans %}Abstract{% endtrans %}</h5>
{% if session.status == 'pending' %}
<p class="pending-notice">{% trans %}This session has NOT been accepted yet. If you would like to see it in the conference, please post it in social networks, as those numbers will be tallied and used as part of the selection criteria{% endtrans %}</p>
{% endif %}
              <p>{{session.abstract | markdown}}</p>
            </div>
            {% if session.video_url %}
            <div class="video">
              <h5>{% trans %}Video{% endtrans %}</h5>
              {{ session.video_url | video_embed }}
            </div>{% endif %}
            {% if session.slide_url %}
            <div class="slide">
              <h5>{% trans %}Slides{% endtrans %}</h5>
              {{ session.slide_url | slide_embed }}
            </div>{% endif %}

            <div class="information">
              <h5>{% trans %}Session Information{% endtrans %}</h5>
              <table>
{% if session.status == 'accepted' %}
                <tr>
                  <td>{% trans %}Confirmed{% endtrans %}</td>
                  <td>{% if session.confirmed %}{% trans %}confirmed{% endtrans %}{% else %}<span class="unconfirmed">{% trans %}unconfirmed{% endtrans %}</span>{% endif %}</td>
                </tr>
{% endif %}
                <tr>
                  <td>{% trans %}Material Level{% endtrans %}</td>
                  <td>{{ _(session.material_level|audlevelname) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Starts On{% endtrans %}</td>
                  <td>{% if session.starts_on %}{{session.starts_on | dateobj | datefmt(locale=lang,tzinfo=conference.timezone)}}{% else %}N/A{% endif %}</td>
                </tr>
                <tr>
                  <td>{% trans %}Room{% endtrans %}</td>
                  <td>{% if session.room %}{{ session.room.name }}{% endif %}</td>
                </tr>
                <tr>
                  <td>{% trans %}Session Duration{% endtrans %}</td>
                  <td>{{ _(session.session_type.name) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Spoken Language{% endtrans %}</td>
                  <td>{{ _(session.spoken_language|langname) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Slide Language{% endtrans %}</td>
                  <td>{{ _(session.slide_language|langname) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Photo Release{% endtrans %}</td>
                  <td>{{ _(session.photo_release|permname) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Recording Release{% endtrans %}</td>
                  <td>{{ _(session.recording_release|permname) }}</td>
                </tr>
                <tr>
                  <td>{% trans %}Materials Release{% endtrans %}</td>
                  <td>{{ _(session.materials_release|permname) }}</td>
                </tr>
              </table>
            </div><!-- .information -->
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock%}

{% block scripts %}
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.7";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
</script>
<script src="https://apis.google.com/js/platform.js" async defer></script>
{% endblock %}