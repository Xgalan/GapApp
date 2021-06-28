$(function() {
    $( "#partnumber-search" ).on('input', function(ev) {
        const searchValue = ev.target.value.toLowerCase();

        if (searchValue=="") {
            $( "tr[data-partnumber]" ).show();
        } else {
            $( "tr[data-partnumber]" ).each(function(i, el) {
                var partnumber = $( el );

                if ( partnumber.data("partnumber").toLowerCase().includes(searchValue) ) {
                    partnumber.show();
                } else {
                    partnumber.hide();
                }
            });
        }
    });
});