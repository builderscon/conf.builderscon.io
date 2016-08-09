{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block header %}
{% include 'session/form_header.tpl' %}
{% endblock %}

{% block scripts %}
{% include 'session/form_scripts.tpl' %}
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
{% with action='/%s/cfp/input' % full_slug %}
{% include "session/form.tpl" %}
{% endwith %}
</main>
{% endblock%}


