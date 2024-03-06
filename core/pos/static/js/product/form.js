$(function () {
    // * Cargamos nuestro plugins de select2
    $('#id_category').select2({
        theme: 'bootstrap4',
        placeholder: 'Seleccione la categoria del producto.',
        language: 'es',
        minimumInputLength: 0,
        ajax: {
            headers: {'X-CSRFToken': csrfToken},
            url: pathname,
            type: 'POST',
            dataType: 'json',
            data: function (params) {
                return {
                    term: params.term,
                    action: 'get_categories_term',
                };
            },
            processResults: function (data, params) {
                return {
                    results: data,
                };
            },
        }
    });

    // * Validamos los campos de entradass
    $('input[name="code"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers_letters');
    });
    $('input[name="names"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });
    $('input[name="pvp"]').TouchSpin({
        min: 0,
        max: 10000,
        step: 0.1,
        decimals: 2,
        prefix: 'S/.'
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'decimals');
    });
    $('input[name="stock"]').TouchSpin({
        min: 0,
        max: 10000,
        step: 1,
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers');
    });
});