{% extends 'layout/conference.tpl' %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <div class="section-content">
        <p>{% trans %}Are you sure you want to delete this session?{% endtrans %}</p>
        <p><strong>{{ session.title }}</strong></p>

        <div class="row">
          <div class="large-3 columns edit-button">
            <form action="/{{ conference.full_slug }}/session/{{ session.id }}/delete" method="POST">
              <input type="hidden" name="delete_token" value="{{ delete_token }}">
              <button id="delete-button" type="submit" class="expanded button">{% trans %}Delete your session/proposal{% endtrans %}</a>
            </form>
          </div>
        </div>

      </div>
    </div>
  </div>
</main>
{% endblock %}
