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

  $("input.title-input").each(function(i, e) {
    if (i > 0) {
      $(e).hide();
    }
  });
  $("#select-title-lang").change(function() {
    var $sel = $("#select-title-lang");

    $("input.title-input").hide();

    var lang = $sel.val();
    var input;
    if (lang == "en") {
      input = $("input[name='title']");
    } else { 
      input = $("input[name='title#"+lang+"']");
    }
    input.show();
  });

  $("textarea.abstract-textarea").each(function(i, e) {
    if (i > 0) {
      $(e).hide();
    }
  });
  $("#select-abstract-lang").change(function() {
    var $sel = $("#select-abstract-lang");

    $("textarea.abstract-textarea").hide();

    var lang = $sel.val();
    var textarea;
    if (lang == "en") {
      textarea = $("textarea[name='abstract']");
    } else { 
      textarea = $("textarea[name='abstract#"+lang+"']");
    }
    textarea.show();
  });
})
-->
</script>

