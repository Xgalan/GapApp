$.fn.extend({
    simpleFilter: function(elementToFilter, dataLabel) {
        const inputEl = this;                                               // i.e.: #searchInput
        const label = dataLabel;                                            // i.e.: "partnumber"
        const elToFilter = elementToFilter + "[data-" + dataLabel + "]";    // i.e.: "tr"
    
        $( inputEl ).on('input', function(ev) {
            const searchValue = ev.target.value.toLowerCase();
    
            if (searchValue=="") {
                $( elToFilter ).show();
            } else {
                $( elToFilter ).each(function(i, el) {
                    var jQel = $( el );
    
                    if ( jQel.data(label).toLowerCase().includes(searchValue) ) {
                        jQel.show();
                    } else {
                        jQel.hide();
                    }
                });
            }
        });
    }
});
