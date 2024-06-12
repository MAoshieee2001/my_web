let input_serice;

$(function () {
    // Capturamos el elemento servicio
    input_serice = $('input[name="is_service"]');

    //  Cargamos nuestro plugins de select2
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

    //  Validamos los campos de entradass
    $('input[name="code"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers_letters');
    });


    //  Validamos los campos de entradass
    $('input[name="purchase"]').TouchSpin({
        min: 0,
        max: 10000,
        step: 0.1,
        decimals: 2,
        prefix: 'S/.'
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'decimals');
    });

    //  Validamos los campos de entradass
    $('input[name="pvp"]').TouchSpin({
        min: 0,
        max: 10000,
        step: 0.1,
        decimals: 2,
        prefix: 'S/.'
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'decimals');
    });

    //  Validamos los campos de entradass
    $('input[name="stock"]').TouchSpin({
        min: 0,
        max: 10000,
        step: 1,
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers');
    });

    // Validamoss para que se oculte y visualize la informacion
    input_serice.change(function (evt) {
        // Capturamos los elementos que vamoss a que ocultarlo
        let container = $('.form-group');
        let container_purchase = container[5];
        let container_stock = container[7];
        // mostramos los container
        container_purchase.style.display = 'block';
        container_stock.style.display = 'block';
        // Validamos si el usuario selecciono el compontenete
        if (this.checked) {
            container_purchase.style.display = 'none';
            container_stock.style.display = 'none';
        }
    });

    input_serice.trigger('change');
});