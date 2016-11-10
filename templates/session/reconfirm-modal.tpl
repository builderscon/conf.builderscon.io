<div class="reveal" id="confirm-modal" data-reveal>
  <p style="margin-right: 3em">{% trans %}Your session {% endtrans %}<strong class="session-title"></strong>{% trans %} will be confirmed when you press the button below{% endtrans %}</p>
  <form id="confirm-form" action="-" method="POST">
    <input type="submit" class="success button" value="{% trans %}Yes, I confirm{% endtrans %}">
  </form>
  <button class="close-button" data-close aria-label="Close modal" type="button">
    <span aria-hidden="true">&times;</span>
  </button>
</div>

