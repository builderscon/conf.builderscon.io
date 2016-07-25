{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
  #contents.index { padding: 180px 0 0 0 }
-->
</style>
{% endblock %}

{% block menuitems %}
<li><a href="/"><span class="i-home"></span></a></li>
<li><a href="http://blog.builderscon.io">BLOG</a></li>
{% endblock %}

{% block hexlogo %}
<div id="hexlogo">
<div class="base"><img src="./assets/images/hex_base.png" /></div><!--  / .base /  -->
<div class="logo"><img src="./assets/images/hex_logo.png" /></div><!--  / .logo /  -->
</div><!--  / #hexlogo /  -->
{% endblock %}

{% block herotext %}
<img src="{{ url('statics', filename='images/builderscon-text.png') }}" width="350">
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Welcome To builderscon{% endtrans %}</h1>
      <div class="section-content">
        <strong>buildersconは「知らなかった、を聞く」をテーマとした技術を愛する全てのギーク達のお祭りです。</strong>

        <p>buildersconではトークに関して技術的な制約はありません、特定のプログラミング言語や技術スタックによるくくりも設けません。</p>

        <p>我々が要求するただ1つのことは、あなたが話すことが、技術者に刺激を与え、興奮させることのみです。
        本カンファレンスのセッションには技術者の血が騒ぐ様なトークを求めています。
        あなたが実装したクレイジーなハックを見せて下さい。あなたの直面した様々な問題と、それをどう解決したかを教えてください。
        未来技術のような未知の領域について教えてください。
        </p>

        <p>是非、buildersconに参加して、あなたの情熱をシェアしてください！我々はあなたの話を聞きたい！</p>
      </div>
    </div>
  </div>

  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Upcoming Conferences{% endtrans %}</h1>
      <div class="section-content">
        <table>
          <tbody>
            {% for conference in conferences %}
            <tr>
              <td>
                <a href="{% if conference.series %}{{ conference.series.slug }}/{% endif %}{{ conference.slug }}">{{ conference.title }}</a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</main>
{% endblock%}
