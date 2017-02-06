  <div class="section article">
    <div class="inner">
{% if not sponsor_header %}
{%   set sponsor_header='Sponsors' %}
{% endif %}
      <h1 class="section-header">{{ _(sponsor_header) }}</h1>
      <div class="section-content">
{% for group in sponsors|groupby('group_name') %}
{%   set perrow = 4 %}
{%   if group.grouper == "tier-2" %}
{%     set perrow = 6 %}
{%   endif %} 
{%   set colsize = (12 / perrow)|int %}
        <div class="row sponsor-tier {{ group.grouper }}">
          <div class="large-12 small-12 columns">
{% for sponsor in group.list %}
{% if loop.index % perrow == 1 %}<div class="row">{% endif %}
            <div class="large-{{ colsize }} small-{{ colsize }} columns">
              <div class="sponsor-slot">
                <a href="{{ sponsor.url }}"><img class="{{ sponsor.group_name }}" src="https://sharaq-dot-builderscon-1248.appspot.com/?preset=sponsor-small&url={{ sponsor.get('logo_url1') or sponsor.get('logo_url') | urlencode }}"></a>
                <div class="sponsor-name"><a href="{{ sponsor.url }}">{{ _(sponsor.name) }}</a></div>
              </div>
            </div>
{% if loop.index % perrow == 0 or loop.last %}</div><!-- end row -->{% endif %}
{% endfor %}
          </div>
        </div>
{% endfor %}
      </div>
    </div>
  </div>

