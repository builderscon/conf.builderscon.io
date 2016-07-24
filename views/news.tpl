{% extends 'base.tpl' %}

{% block heroimage %}{% endblock %}

{% block main %}
<main>
  <div class="section article">
    <div class="inner">
      <h1 class="section-header">Recent News</h1>
      <div class="section-content">
        <div class="post-content">
          <ul class="post-list">
          {% for entry in entries %}
            <li>
              <span class="post-meta">{{ entry.date }}</span>
              <h2>
                <a class="post-link" href="{{ entry.link }}">{{ entry.title }}</a>
              </h2>
            </li>
          {% endfor %}
          </ul>
        </div>
      </div>
    </div>
  </div>
</main>
{% endblock %}
