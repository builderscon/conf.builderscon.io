{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h3>{{ conference.sub_title }}</h3>
<h3>{% if conference.dates|length == 1 %}{{ conference.dates[0].date }}{% endif %}</h3>
{% endblock %}

{% block header %}
<style type="text/css">
<!--
.cfp-form .error {
  color: #f00;
  font-weight: bold;
}

.cfp-form label {
  font-weight: bold;
  font-size: 1.1em;
}

.cfp-form .row {
  margin-bottom: 0.5em;
}

.yes-no {
  padding: 2px;
  font-weight: bold;
}

.notice-small {
  font-size: 80% !important;
  color: #888 !important;
}

.tos-agreement {
  border: 2px dotted #f99;
}

.tos-agreement * {
  padding: 10px !important;
}

-->
</style>
{% endblock %}

{% block main %}
<main>
{% if not errors %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Call For Papers</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-12 columns"><h3>概要説明</h3></div>
        </div>
        <div class="row">
          <div class="large-12 columns">
            <p>buildersconはスピーカー達のトークが最大の武器です。あなたのバックグラウンドがどんなものであろうと、
            他の参加者の皆様と技術への愛をシェアしていただける方であれば大歓迎です。どの専門分野を持っていても、
            どの技術コミュニティからの参加であっても歓迎します。</p>

            <p>builderscon自体がどんなカンファレンスを目指しているかは<a href="/" target="_blank">builderscon ホーム</a>
            および<a href="/" target="_blank">builderscon tokyo 2016</a>のページをご覧ください。</p>

            </p>buildersconではトークに関して技術的な制約はありません、特定のプログラミング言語や技術スタックによるくくりも設けません。
            必要なのは技術者達に刺激を与えワクワクさせてくれるアイデアのみです。
            あなたが実装したクレイジーなハックを見せて下さい。あなたの好きな言語のディープな知識をシェアしてください。
            あなたの直面した様々な問題と、それをどう解決したかを教えてください。未来技術のような未知の領域について教えてください。</p>

            <p>注意点として、あるサイト、プロダクト、フレームワーク、新技術の紹介「だけ」に終始するトークはあまりbuildersconにはふさわしくありません、
            こういった事柄をトークの題材にする場合には上にあるように、あなたがどういう問題に直面し、どう解決したか伝えるようにするといいでしょう。</p>

            <p>buildersconの参加者は、あなたと同じく技術に対する愛に溢れた人々です。あなたが提供してくれる「知らなかった、を聞く」チャンスををワクワクしながら待っています。
            是非、buildersconに参加して、あなたの情熱をシェアしてください！</p>

            <p>応募は以下のフォームに入力して、「{% trans %}Submit your proposal{% endtrans %}」ボタンを押してください。</p>
          </div>
        </div>
      </div><!-- section-content -->
    </div><!-- inner -->
  </div><!-- section article -->
{% endif %}

{% set left = 3 %}
{% set right = 12 - left %}
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Submission Form{% endtrans %}</h1>
      <div class="section-content">
        <form class="cfp-form" action="/{{ full_slug }}/cfp/input" method="post">
          <div class="row">
            <div class="large-12 columns"><h3>{% trans %}Proposal Details{% endtrans %}</h3></div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns">
              <label>Title</label>
              <div>{% trans %}You must provide at least one title in any of the supported languages{% endtrans %}</div>
              {% if errors and missing.get('title') %}<span class="error">{% trans %}required field{% endtrans %}</span>{% endif %}
            </div>
            <div class="large-{{ right }} columns">
{% for l in languages %}
{% set itemName = 'title#' + l.value if l.value != 'en' else 'title' %}
              <div class="row" style="margin-left: 0em">
                <div class="large-11 columns">
                  <input type="text" name="{{ itemName }}"{% if session %} value="{{ session.get(itemName, '') }}"{% endif %}/>
                </div>
                <div class="large-1 columns" style="text-align: right">
                  <span style="padding: 2px; font-size: 60%; border: 1px solid #0b0; background-color: #0c0">{{ _(l.name) }}</span>
                </div>
              </div>
{% endfor %}
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns">
              <label>Session type</label>
              {% if errors and missing.get('session_type_id') %}<span class="error">{% trans %}required field{% endtrans %}</span>{% endif %}
            </div>
            <div class="large-{{ right }} columns">
<input type="hidden" name="session_type" value="2ab88532-5ad6-11e6-afb8-42010af00793">
              <!--select name="session_type">
{% for stype in session_types %}
                <option value="{{ stype.id }}"{% if stype.is_accepting_submission %}{% if loop.first %} selected="selected"{% endif %}{% else %} disabled="disabled"{% endif %}>{{ stype.name }}{% if not stype.is_accepting_submission %} [{% trans %}SUBMISSION CURRENTLY CLOSED{% endtrans %}]{% endif %}</option>
{% endfor %}
              </select-->
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns">
              <label>Abstract</label>
              <div>{% trans %}You must provide at least one abstract in any of the supported languages{% endtrans %}</div>
              {% if errors and missing.get('abstract') %}<span class="error">{% trans %}required field{% endtrans %}</span>{% endif %}
            </div>
            <div class="large-{{ right }} columns">
{% for l in languages %}
{% set itemName = 'abstract#' + l.value if l.value != 'en' else 'abstract' %}
              <div class="row" style="margin-left: 0em">
                <div class="large-11 columns">
                  <textarea name="{{ itemName }}" rows=8>{% if session %}{{ session.get(itemName, '') }}{% endif %}</textarea>
                </div>
                <div class="large-1 columns" style="text-align: right">
                  <span style="padding: 2px; font-size: 60%; border: 1px solid #0b0; background-color: #0c0">{{ _(l.name) }}</span>
                </div>
              </div>
{% endfor %}
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Expected audience level</label></div>
            <div class="large-{{ right }} columns">
{% set sel_material_level = session.get('material_level', 'beginner') if session else 'beginner' %}
              <select name="material_level">
{% set levels = [
  { 'name': 'Beginner', 'value': 'beginner' },
  { 'name': 'Intermediate', 'value': 'intermediate' },
  { 'name': 'Expert', 'value': 'expert' }
] %}
{% for level in levels %}
                <option value="{{ level.value }}" id="{{ level.value }}"{% if level.value == sel_material_level %} selected="selected"{% endif %}/><label for="{{ level.value }}">{{ _(level.name) }}</option>
{% endfor %}
              </select>
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Spoken language</label></div>
            <div class="large-{{ right }} columns">
              <select name="spoken_language">
{% set sel_spoken_language = session.get('spoken_language', 'en') if session else 'en' %}
{% for l in languages %}
                <option value="{{ l.value }}"{% if l.value == sel_spoken_language %} selected="selected"{% endif %}>{{ _(l.name) }}</option>
{% endfor %}
              </select>
              <p class="notice-small">Please select which language you will be speaking in.</p>
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Slide Language</label></div>
            <div class="large-{{ right }} columns">
              <select name="slide_language">
{% set sel_slide_language = session.get('slide_language', 'en') if session else 'en' %}
{% for l in languages %}
                <option value="{{ l.value }}"{% if l.value == sel_slide_language %} selected="selected"{% endif %}>{{ _(l.name) }}</option>
{% endfor %}
              </select>
              <p class="notice-small">Please select which language you will write your slides in.</p>
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Comments</label></div>
            <div class="large-{{ right }} columns">
              <textarea name="memo" rows=4 placeholder="{% trans %}Specify any communication that you might want to relay to the organizer: e.g. special financial requirements, required documents, specific dates during the conference you might not be able to attend, etc{% endtrans %}">{% if session %}{{ session.get('memo', '') }}{% endif %}</textarea>

            </div>
          </div>
          <div class="row">
            <div class="large-12 columns">
              <h3>{% trans %}Videos and Photos{% endtrans %}</h3>
              <p class="notice-small">Please refer to our <a href="." target="_blank">terms of use</a> about how builderscon uses videos, photos, and other materials.</p>
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Photo Release</label></div>
            <div class="large-{{ right }} columns">
              <p>By selecting "yes" to this, you agree to have your photo taken by our staff during your presentation, and to allow builderscon to distribute those photos and to place them on our website(s).</p>
{% set sel_photo_permission = session.get('photo_permission', 'allow') if session else 'allow' %}
{% set photo_permission_choices = [
    {'name': 'Yes', 'value': 'allow' },
    {'name': 'No', 'value': 'disallow' }
] %}
{% for choice in photo_permission_choices %}
              <input type="radio" name="photo_permission" value="{{ choice.value }}"{% if sel_photo_permission == choice.value %} checked="checked"{% endif %}/><span class="yes-no">{{ _(choice.name) }}</span>
{% endfor %}
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Recording Release</label></div>
            <div class="large-{{ right }} columns">
              <p>By selecting "yes" to this, you agree to have your presentation recorded by our staff, and to allow builderscon to distribute those recordings and to place them on our website(s).</p>
{% set sel_video_permission = session.get('video_permission', 'allow') if session else 'allow' %}
{% set video_permission_choices = [
    {'name': 'Yes', 'value': 'allow' },
    {'name': 'No', 'value': 'disallow' }
] %}
{% for choice in video_permission_choices %}
              <input type="radio" name="video_permission" value="{{ choice.value }}"{% if sel_video_permission == choice.value %} checked="checked"{% endif %}/><span class="yes-no">{{ _(choice.name) }}</span>
{% endfor %}
            </div>
          </div>
          <div class="row">
            <div class="large-{{ left }} columns"><label>Materials Release</label></div>
            <div class="large-{{ right }} columns">
              <p>By selecting "yes" to this, you agree to release materials from your presentation (such as slides), and to allow builderscon to distribute those materials and to place them on our website(s).</p>
{% set sel_material_release = session.get('materials_release', 'allow') if session else 'allow' %}
{% set material_release_choices = [
    {'name': 'Yes', 'value': 'allow' },
    {'name': 'No', 'value': 'disallow' }
] %}
{% for choice in material_release_choices %}
              <input type="radio" name="materials_release" value="{{ choice.value }}"{% if sel_material_release == choice.value %} checked="checked"{% endif %}/><span class="yes-no">{{ _(choice.name) }}</span>
{% endfor %}
            </div>
          </div>
          <div class="row tos-agreement">
            <div class="large-12 columns">
              <p>I hereby confirm that I understand and agree to the <a href="" target="_blank">terms of use</a> and the various release agreements described with regards to submitting a proposal for builderscon.</p>
              <input type="checkbox" name="terms_of_use" value=true id="terms_of_use_yes" onchange="handleTermsOfUseAgree(this);" /> <span class="yes-no">{% trans %}Yes{% endtrans %}</span>
            </div>
          </div>
          <div class="row">
            <div class="large-12 columns">
              <button id="submit-button" type="submit" class="expanded button disabled" disabled="disabled">{% trans %}Submit your proposal{% endtrans %}</button>
              <p class="notice-small">Please check &#34;Yes&#34; above to agree to terms of use, before submitting your proposal.</p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
{% endblock%}

{% block scripts %}
<script>
<!--
$(function() {
  $("#terms_of_use_yes").change(function() {
    $btn = $("#submit-button")
    if ($("#terms_of_use_yes").prop('checked')) {
      $btn.removeClass("disabled");
      $btn.prop("disabled", false)
    } else {
      $btn.addClass("disabled")
      $btn.prop("disabled", true)
    }
  });
})
-->
</script>
{% endblock %}
