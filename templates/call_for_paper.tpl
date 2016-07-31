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
      <h1 class="section-header">Guidelines</h1>
      <div class="section-content">
        <div style="margin: 20px 0px;">
          <h3>Application method</h3>
          <ul>
            <li>Fill in the above form and press the 	&#34;{% trans %}Submit your proposal{% endtrans %}	&#34; button</li>
          </ul>
          <h3>Subject</h3>
            <ul>
              <li>For more background and purposes of builderscon,  please go to <a href="/">Home</a> and <a href="/">{{ conference.title }}</a></li>
              <li>builderscon is a tech-agnostic, polyglot conference, so there is no restriction on what programming language or technology stack your session is about.</li>
              <li>Examples of good talk subjects, not limited to the below, could be:
                <ul>
                  <li>"How we built X (obstacles that we faced, and how we solved them)"</li>
                  <li>"Discussion about technologies behind X (which ones were chosen, why they were chosen, and problems, if any)"</li>
                </ul>
              </li>
              <li>Talks which <strong>only</strong> introduces new websites, products, frameworks or technologies are not suitable for builderson,
              thus if you talk about those subjects, you should talk about what challenges you overcame and how</li>
            </ul>
          <h3>Proposal acceptance notification</h3>
            <p>mail...? how do we notify speakers?</p>
          <h3>Speaker confirmation on acceptance notification</h3>
            <p>The speaker of an accepted talk proposal needs to confirm whether to present at the conference, until 2016 xxx.
            If the speaker does not confirm by that time, we treat the talk proposal as rejected.</p>
          <h3>Timeline until the conference date</h3>
            <p>coming soon</p>
          <h3>Session types</h3>
            <ul>
              <li>30 mins x ? slots</li>
              <li>15 mins x ? slots</li>
            </ul>
          <h3>Conference Ticket for Speakers</h3>
            <p>anything special?</p>
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
