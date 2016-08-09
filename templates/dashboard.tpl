{% extends 'layout/base.tpl' %}

{% block header %}
<style type="text/css">
<!--
div.profile {
  padding: 5px;
}
div.profile img {
  padding: 2px;
  border: 1px solid #ccc;
}
div.profile p.name {
  text-align: center;
}
span.auth_via {
  border: 1px solid #0a0;
  background-color: #cfc;
  font-weight: bold;
  font-size: 0.6em;
  color: #0a0;
  padding: 0.2em;
}
div.profile-content {
  padding-left: 1em;
}
div.conference-history {
  padding-left: 2em;
}

.invalid {
  color: #ccc;
}

-->
</style>
{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <div class="section-content no-header">

        <div class="row">
          <div class="large-2 columns">
            <div class="profile">
              <img src="{{ user.avatar_url }}">
              <p class="name">{{ user.nickname }} <span class="auth_via">{{ user.auth_via }}</span></p>
            </div>
          </div>
          <div class="profile-content large-10 columns">
{% if conferences %}
            <h3>{% trans %}Organizer{% endtrans %}</h3>
            <div class="conference-history">
{% for conference in conferences %}
              <div class="row">
                <div class="large-3 columns"><a href="/{{ conference.series.slug }}/{{ conference.slug }}">{{ conference.title }}</a></div>
              </div>
{% endfor %}
            </div>
{% endif %}

            <h3>Proposals</h3>
{% if not proposals %}
            <p>{% trans %}No proposals have been submitted{% endtrans %}</p>
{% else %}
            <table class="proposal-history">
            <thead>
              <tr>
                <td>{% trans %}Title{% endtrans %}</td>
                <td>&nbsp;</td>
              </tr>
            </thead>
            <tbody>
{% for proposal in proposals %}
              <tr>
                <td><span{% if proposal.conference.status == 'private' %} class="invalid"{% endif %}>{{ proposal.title or 'N/A' }}</span></td>
                <td><a href="/session/edit?id={{ proposal.id }}">{% trans %}Edit{% endtrans %}</a></td>
              </tr>
{% endfor %}
            </tbody>
            </table>
{% endif %}
          </div>
        </div>

      </div><!-- section-content -->
    </div><!-- inner -->
  </div><!-- section -->
</main>
{% endblock %}
