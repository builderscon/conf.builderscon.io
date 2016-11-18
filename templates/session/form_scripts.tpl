<script>
<!--
$(function() {
  $("#terms_of_use_yes").change(function() {
    var $btn = $("#submit-button");
    if ($("#terms_of_use_yes").prop('checked')) {
      $btn.removeClass("disabled");
      $btn.prop("disabled", false);
    } else {
      $btn.addClass("disabled");
      $btn.prop("disabled", true);
    }
  });

  $("#cfptabs").foundation("selectTab", "#panel-{{ lang }}");

  $("#select-material-level").val("{% if session %}{{ session.get('material_level', lang) }}{% else %}{{ lang }}{% endif %}");
  $("#select-spoken-language").val("{% if session %}{{ session.get('spoken_language', lang) }}{% else %}{{ lang }}{% endif %}");
  $("#select-slide-language").val("{% if session %}{{ session.get('slide_language', lang) }}{% else %}{{ lang }}{% endif %}");
})
-->
</script>

