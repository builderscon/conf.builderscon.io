{% extends 'layout/base.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block herotext %}
<h1>{{ conference.title }}</h1>
<h3>{{ conference.sub_title }}</h3>
<h3>{% if conference.dates|length == 1 %}{{ conference.dates[0].date }}{% endif %}</h3>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Proposal submission</h1>
      <div class="section-content">
        <form action="." method="post">
          <div class="row">
            <h3概要説明</h3>
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
            是非、buildersconに参加して、あなたの情熱をシェアしてください！我々はあなたの話を聞きたい！</p>
          </div>
          <div class="row">
            <h3>応募方法</h3>
            <ul>
              <li>以下のフォームに入力して、&#34;{% trans %}Submit your proposal{% endtrans %}&#34;ボタンを押してください。</li>
            </ul>
          </div>
          <div class="row">
            <h3>Videos and photos</h3>
            <div class="large-12 columns">
              <label>Can we record videos?</label>
              <input type="radio" name="video_permission" value="allow"    id="video_permission_allow" checked/><label for="video_permission_allow">Yes</label>
              <input type="radio" name="video_permission" value="disallow" id="video_permission_disallow"     /><label for="video_permission_disallow">No</label>
            </div>
            <div class="large-12 columns">
              <label>Can we take photos?</label>
              <input type="radio" name="photo_permission" value="allow"    id="photo_permission_allow" checked/><label for="photo_permission_allow">Yes</label>
              <input type="radio" name="photo_permission" value="disallow" id="photo_permission_disallow" /><label for="photo_permission_disallow">No</label>
            </div>
            <div class="large-12 columns">
              <p>Please refer to <a href="." target="_blank">terms of use</a> about how builderscon uses videos and photos.</p>
            </div>
          </div>
          <div class="row">
            <h3>Language</h3>
            <div class="large-12 columns">
              <label>Spoken language</label>
              <input type="radio" name="spoken_language" value="en" id="spoken_language_en" checked/><label for="spoken_language_en">English</label>
              <input type="radio" name="spoken_language" value="jp" id="spoken_language_jp" /><label for="spoken_language_jp">Japanese</label>
            </div>
            <div class="large-12 columns">
              <label>Slides' language</label>
              <input type="radio" name="slide_language" value="en"  id="slide_language_en" checked/><label for="slide_language_en">English</label>
              <input type="radio" name="slide_language" value="jp"  id="slide_language_jp" /><label for="slide_language_jp">Japanese</label>
            </div>
          </div>
          <div class="row">
            <h3>Proposal</h3>
            <div class="large-12 columns">
              <label>Title<input type="text" name="title"/></label>
            </div>
            <div class="large-12 columns">
              <label>Abstract<textarea name="abstract" rows=8></textarea></label>
            </div>
            <div class="large-12 columns">
              <label>Session type</label>
              <select name="session_type">
                <option value="15" id="session_type_15min" selected/><label for="session_type_15min">15 minutes</option>
                <option value="30" id="session_type_30min"         /><label for="session_type_30min">30 minutes</option>
              </select>
            </div>
            <div class="large-12 columns">
              <label>Expected audience level</label>
              <select name="material_level">
                <option value="beginner"     id="beginner"     selected/><label for="beginner"    >Beginners</option>
                <option value="intermediate" id="intermediate"         /><label for="intermediate">Intermediate</option>
                <option value="expert"       id="expert"               /><label for="expert"      >Advanced</option>
              </select>
            </div>
          </div>
          <div class="row">
            <h3>Comments</h3>
            <div class="large-12 columns">
              <label>Other comments for the organizer - (e.g.) you can be present on the 1st day of the conference, but not on the 2nd day.
                <textarea name="memo" rows=4 placeholder""></textarea>
              </label>
            </div>
          </div>
          <div class="row">
            <h3>Proposal submission</h3>
            <div class="large-12 columns">
              <label>I hereby confirm that I understand and agree to each and all of the <a href="" target="_blank">terms of use</a> regarding submitting a proposal for builderscon.</label>
              <input type="checkbox" name="terms_of_use" value=true id="terms_of_use_yes" onchange="handleTermsOfUseAgree(this);" /><label for="terms_of_use_yes">Yes</label>
            </div>
            <div class="large-12 columns" style="margin-top: 2em">
               <div>
                 <p>Please check &#34;Yes&#34; above to agree to terms of use, before submitting your proposal.</p>
               </div>
               <button id="submit-button" type="submit" class="expanded button disabled">{% trans %}Submit your proposal{% endtrans %}</a>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div class="section article">
    <div class="inner">
      <h1 class="section-header">プロポーザル送信後の流れ</h1>
      <div class="section-content">
        <div style="margin: 20px 0px;">
          <h4>プロポーザル受理の確認、修正</h4>
          <p>応募者がプロポーザルを送信した後は、主催者はメールにてプロポーザルが受理されたことを連絡します。
          応募者は<a href="." target="_blank">こちらのページ</a>にアクセスして自身のプロポーザルを閲覧することができ、
          また締切日(octavとリンク)前までは自分のプロポーザルを修正することができます。</p>
          <h4>プロポーザルの採択通知</h4>
          <p>プロポーザル受理の締め切り(octavとリンク)日ののちに、審査期間を経て、主催者はメールにて採択されたスピーカーに採択通知を送ります。
          また<a href="." target="_blank">セッション一覧のページ</a>にて採択されたトークを発表します。セッション一覧に自分のトークが採択されているのに、
          採択通知を受け取っていないスピーカーは速やかに主催者にメールで連絡してください。</p>
          <h4>採択されたスピーカー者による登壇可否の確認</h4>
          <p>採択通知を受け取ったスピーカーは必ず○○日(octavとリンク)までに、採択された枠で登壇可能であることを主催者に通達してください。
          主催者への登壇可否の通達は、採択通知のメールに返信する形で行ってください。
          期限の○○日(octavとリンク)までにスピーカーからの登壇可否の確認がなかった場合、主催者は当該の応募については不採用になったものとして取り扱います。<p>
          <h4>急な事情による不参加</h4>
          <p>登壇確認をしたのちに、やむを得ない事情により登壇ができなくなった場合は、 スピーカーは速やかにメールにて主催者に連絡してください。</p>
          <h4>スピーカー向けチケットの特典</h4>
          <p>TBD</p>
          <h4>カンファレンス当日</h4>
          <p>カンファレンス当日は、時間に余裕をもって会場までお越しください。リラックスして、あなたの素晴らしいトークを思う存分披露してください。</p>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock%}

{% block scripts %}
<script>
  function handleTermsOfUseAgree(element){
    if(element.checked)
      document.getElementById("submit-button").className = "expanded button";
    else
      document.getElementById("submit-button").className = "expanded button disabled";
  }
</script>
{% endblock %}
