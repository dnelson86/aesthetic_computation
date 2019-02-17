// dnelson
// aesthetic computation

(function($) {

    // toggle 'main menu'
    $( '.stripe-menu' ).on( 'click', function() {
        $(this).toggleClass('close');
        $('.site-branding').toggleClass('hide');
        $('.site-navigation').toggleClass('show');
        $('.site-header').toggleClass('no-shadow');
        return false; // stop proapagation
    });

    // close 'main menu' for any global click which bubbles this far
    $(document).click(function(e) {
      // only if outside
      if( $(e.target).parents('.site-navigation').length )
      {
        return;
      }

      // only if already open
      if( $('.stripe-menu').hasClass('close') )
      {
          $('.stripe-menu').toggleClass('close');
          $('.site-branding').toggleClass('hide');
          $('.site-navigation').toggleClass('show');
          $('.site-header').toggleClass('no-shadow');
      }
    });

    // individual post page: arrow keys trigger page-redirect navigation
    var prev_link = $("#prev_link");
    var next_link = $("#next_link");

    $(document).keyup(function(e) {
      if (e.keyCode == 37) { // left arrow
        if (prev_link) {
          window.location.replace(prev_link.attr("href"));
        }
      }

      if (e.keyCode == 39) { // right arrow
        if (next_link) {
          window.location.replace(next_link.attr("href"));
        }
      }

    });

})(jQuery);
