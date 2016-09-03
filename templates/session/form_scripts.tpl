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

  $("#select-spoken-language").val("{{ lang }}");
  $("#select-slide-language").val("{{ lang }}");
})
-->
</script>

