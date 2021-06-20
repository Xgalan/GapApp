function arrayIsEmpty(arr) {
    if (Array.isArray(arr) && !arr.length) {
        return true;
    }
};

$(function() {
    const frmSearch = "#frmSearch";
    var selectSearch = $( "#sel-partnumber-search" );

    selectSearch.select2({
        placeholder: 'Cerca codice...',
        minimumInputLength: 2,
        theme: "bootstrap4",
        ajax: {
            dataType: 'json',
            data: function (params) {
                var query = {
                  search: params.term
                }
                return query;
            },
            processResults: function(data) {
                return {
                    results: $.map(data.results, function(obj) {
                        return {
                            id: obj.id,
                            text: obj.sku
                        };
                    })
                };
            }
        }
    });

    $( frmSearch ).submit(function( event ) {
        event.preventDefault();

        const searchVal = selectSearch[0].value;
        const urlSearch = `/api/partnumbers/${searchVal}/print_detail`;
        $( this ).attr('action', urlSearch);
        $( this )[0].submit();
    });
});
