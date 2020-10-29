function arrayIsEmpty(arr) {
    if (Array.isArray(arr) && !arr.length) {
        return true;
    }
};

// HTML Escape helper utility
var util = (function () {
    // Thanks to Andrea Giammarchi
    var
        reEscape = /[&<>'"]/g,
        reUnescape = /&(?:amp|#38|lt|#60|gt|#62|apos|#39|quot|#34);/g,
        oEscape = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
        },
        oUnescape = {
        '&amp;': '&',
        '&#38;': '&',
        '&lt;': '<',
        '&#60;': '<',
        '&gt;': '>',
        '&#62;': '>',
        '&apos;': "'",
        '&#39;': "'",
        '&quot;': '"',
        '&#34;': '"'
        },
        fnEscape = function (m) {
        return oEscape[m];
        },
        fnUnescape = function (m) {
        return oUnescape[m];
        },
        replace = String.prototype.replace
    ;
    return (Object.freeze || Object)({
        escape: function escape(s) {
        return replace.call(s, reEscape, fnEscape);
        },
        unescape: function unescape(s) {
        return replace.call(s, reUnescape, fnUnescape);
        }
    });
    }());
 
// Tagged template function
function html(pieces) {
    var result = pieces[0];
    var substitutions = [].slice.call(arguments, 1);
    for (var i = 0; i < substitutions.length; ++i) {
        result += util.escape(substitutions[i]) + pieces[i + 1];
    }

    return result;
};


$(function() {
    const frmSearch = "#frmSearch";
    var selectSearch = $( "select[name='search']" );

    selectSearch.select2({
        placeholder: 'Cerca codice...',
        minimumInputLength: 2,
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
                    results: $.map(data, function(obj) {
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

        const searchVal = $( this ).serializeArray()[0];
        const urlSearch = `/partnumbers/print/${searchVal.value}`;
        $( this ).attr('action', urlSearch);
        $( this )[0].submit();
      });
});