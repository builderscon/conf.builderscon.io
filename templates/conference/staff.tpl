{% extends 'layout/conference.tpl' %}

{% block title %}{% trans %}Staff{% endtrans%}: {{ conference.title }} - builderscon{% endblock %}

{% block heroimage %}
<div id="heroimage-empty"></div>
{% endblock %}

{% macro list_staff(staff) %}
{%- for user in staff %}
{%- if loop.index % 6 == 1 %}
      <div class="row">
{% endif -%}
        <div class="staff large-2 small-2 columns{%- if loop.last or loop.index % 6 == 0 %} end{% endif %}">
            <img class="avatar" src="{{ user.avatar_url }}">
            <p class="nickname"><a href="/user/{{ user.id }}">{{ user.nickname }}</a></p>
        </div>
{%- if loop.last or loop.index % 6 == 0 %}
      </div>
{% endif -%}
{% endfor %}
{% endmacro %}

{% block main %}
{% set avatar_edge = 100 %}
<style type="text/css">
<!--
    div.staff {
        text-align: center;
    }
    div.staff p.nickname {
        text-align: center;
    }
    div.staff img.avatar {
        border-radius: {{ avatar_edge / 2 }}px;
        width: {{ avatar_edge }}px;
        height: {{ avatar_edge }}px;
    }
-->
</style>


<div class="section article">
  <div class="inner">
    <h1 class="section-header">{% trans %}Staff{% endtrans %} - {{ conference.title }}</h1>
    <div class="section-content">
      {{ list_staff(conference.administrators) }}
      {{ list_staff(staff) }}
    </div>
  </div>
</div>
{% endblock %}
