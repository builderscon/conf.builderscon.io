{% extends 'layout/base.tpl' %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <div class="section-content no-header">
        <form action="add" method="POST">
          <div class="row">
            <label for="">
              title
              <input name="proposal_title" type="text" value=""/>
            </label>
          </div>
          <div class="row">
            <label for="">
              detail
              <textarea cols="30" id="proposal_detail" name="proposal_detail" rows="10"></textarea>
            </label>
          </div>
          <div class="row">
            <button class="expanded button" href="">{% trans %}Submit{% endtrans %}</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
{% endblock%}
