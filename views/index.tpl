{% extends 'layout/base.tpl' %}

{% block herotext %}
<h1>builderscon</h1>
<h2>Discover Something New</h2>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">buildersconへようこそ&#33;</h1>
      <div class="section-content">

        <h3>buildersconは技術を愛する全てのギーク達のお祭りです。</h3>

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
      <h1 class="section-header">Conferences</h1>
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
