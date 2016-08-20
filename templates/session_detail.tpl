{% extends 'layout/base.tpl' %}

{% block main %}
<div id="fb-root"></div>
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{{session.title}}</h1>
      <div class="section-content">

        <div class="row">
          <div class="text-center large-2 columns">
            <img style="width: 120px; height: 120px; border: 1px solid #ccc" src="{% if session.speaker.avatar_url %}{{ session.speaker.avatar_url }}{% else %}{{ url('static', filename='images/noprofile.png') }}{% endif %}" />
            <div class="text-center">
              <a  href="." target="_blank">{{session.speaker.nickname}}</a>
            </div>
            <div class="social-button">
              <a href="http://b.hatena.ne.jp/entry/" class="hatena-bookmark-button" data-hatena-bookmark-layout="vertical-balloon" data-hatena-bookmark-lang="ja" title="このエントリーをはてなブックマークに追加"><img src="https://b.st-hatena.com/images/entry-button/button-only@2x.png" alt="このエントリーをはてなブックマークに追加" width="20" height="20" style="border: none;" /></a><script type="text/javascript" src="https://b.st-hatena.com/js/bookmark_button.js" charset="utf-8" async="async"></script>
            </div>
            <div class="social-button">
              <div class="g-plusone" data-size="tall"  data-href="{{url}}"></div>
            </div>
            <div class="social-button">
              <div class="fb-like" data-href="{{url}}" data-layout="box_count" data-action="like" data-size="large" data-show-faces="false" data-share="false"></div>
            </div>
            <div class="social-button">
              <a href="https://twitter.com/share" class="twitter-share-button" data-size="large">Tweet</a>
            </div>

            <!-- add new buttons here e.g. edit session details button -->

          </div>
          <div class="large-10 columns">
            <p>
              {{session.abstract | markdown}}
            </p>
          </div>
        </div>

        <div class="row">
          <table>
            <tr>
              <td>Material Level</td>
              <td>{{session.material_level}}</td>
            </tr>
{% if session.starts_on %}
            <tr>
              <td>Starts On</td>
              <td>{{session.starts_on}}</td>
            </tr>
{% endif %}
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