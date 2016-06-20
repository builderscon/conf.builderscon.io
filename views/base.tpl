<!doctype html>
<html lang="ja">
  <head>
    <title>builderscon::{{ pagetitle }}</title>
    {% include "meta.tpl" %}
  </head>
  <body>
    <div id="wrapper">
      {% include "header.tpl" %}
      {% include "eyecatch.tpl" %}
      <div id="contents" class="index">
        {% block main %}
        {% endblock%}
      </div>
      {% include "pagetop.tpl" %}
      {% include "footer.tpl" %}
    </div>
    {% include "footer_scripts.tpl" %}
  </body>
</html>
