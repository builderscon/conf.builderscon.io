<script>
<!--
$(function() {
  $(document).ready(function() {
    $(".confirm-button").click(function(e) {
      var $t = $(e.target);
      var id = $t.attr('data-id');
      var title = $t.attr('data-title');
      var $f = $("#confirm-form");
      $f.attr('action', '/{{ conference.full_slug }}/session/' + id + '/confirm');
      $("strong.session-title", "#confirm-modal").text(decodeURI(title));
      $("#confirm-modal").foundation("open");
      return false;
    });
  });
})
-->
</script>

