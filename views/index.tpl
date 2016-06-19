{% extends 'base.tpl' %}

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
                <a href="{{ conference.series.slug }}/{{ conference.slug }}">
                  {{ conference.title }}
                </a>
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
