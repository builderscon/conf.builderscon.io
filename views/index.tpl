{% extends 'base.tpl' %}

{% block herotext %}
<h1>Conferences</h1>
<h2>Here you can find upcoming conferences from our partners</h2>
<h2>buildersconおよびパートナー団体が運営するカンファレンス</h2>
{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Conferences</h1>
      <div class="section-content">
        <table>
          <tbody>
            {% for conference in conferences %}
            <tr>
              <td>
                <a href="{% if confnerence.series %}{{ conference.series.slug }}/{% endif %}{{ conference.slug }}">{{ conference.title }}</a>
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
