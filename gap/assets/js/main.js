function arrayIsEmpty(arr) {
    if (Array.isArray(arr) && !arr.length) {
        return true;
    }
}

function ready(fn) {
    if (document.readyState !== 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

function selectOption(elementId) {
    // elementID must be a string prepended with '#'
    const selectEl = document.querySelector(elementId);
    for (const [key, value] of Object.entries(selectEl.options)) {
        if (value.value == selectEl.dataset.selected) {
            selectEl.options.selectedIndex = key;
        }
    }
}
