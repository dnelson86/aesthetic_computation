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

    // detect touch swipes
    $(this).bind('touchstart', touchstart);
      
    function touchstart(event) {
      var touches = event.originalEvent.touches;
      if (touches && touches.length) {
        startX = touches[0].pageX;
        startY = touches[0].pageY;
        $(this).bind('touchmove', touchmove);
        $(this).bind('touchend', touchend);
      }
      event.preventDefault();
    }
      
    function touchmove(event) {
      var touches = event.originalEvent.touches;
      if (touches && touches.length) {
        var deltaX = startX - touches[0].pageX;
        var deltaY = startY - touches[0].pageY;
          
        if (deltaX >= 50) {
          //$this.trigger("swipeLeft");
          // individual post page: arrow keys trigger page-redirect navigation
          var prev_link = $("#prev_link");
          if (prev_link) {
            window.location.replace(prev_link.attr("href"));
          }
        }

        if (deltaX <= -50) {
          // individual post page: arrow keys trigger page-redirect navigation
          var next_link = $("#next_link");
          if (next_link) {
            window.location.replace(next_link.attr("href"));
          }
          //$this.trigger("swipeRight");
        }

        //if (deltaY >= 50) {
        //  $this.trigger("swipeUp");
        //}

        //if (deltaY <= -50) {
        //  $this.trigger("swipeDown");
        //}

        if (Math.abs(deltaX) >= 50 || Math.abs(deltaY) >= 50) {
          $(this).unbind('touchmove', touchmove);
          $(this).unbind('touchend', touchend);
        }
      }
      event.preventDefault();
    }
      
    function touchend(event) {
      $(this).unbind('touchmove', touchmove);
      event.preventDefault();
    }
      

})(jQuery);
