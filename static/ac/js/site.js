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

})(jQuery);
