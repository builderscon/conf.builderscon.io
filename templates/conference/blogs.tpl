{% extends 'layout/conference.tpl' %}

{% block title %}{% trans %}Feedback - Blogs{% endtrans%}: {{ conference.title }} - builderscon{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Feedback - Blogs{% endtrans %}: {{ conference.title }}</h1>
      <div class="section-content">
        <div class="row">
          <div class="large-12 small-12 columns">{{ _("%(count)d blogs collected", count=blog_entries | length) }}</div>
        </div>
        <div class="row">
          <div class="large-12 small-12 columns">
{% if blog_entries | length > 0 %}
            <ol class="visited-link">
{% for entry in blog_entries %}
              <li><a target="_blank" href="{{ entry.url }}">{{ entry.title }}</a></li>
{% endfor %}
            </ol>
{% endif %}
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock %}
