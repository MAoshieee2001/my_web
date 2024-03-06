let input_dni, input_first, input_last;

$(function () {
    input_dni = $('input[name="dni"]');
    input_first = $('input[name="first_names"]');
    input_last = $('input[name="last_names"]');

    $('#id_gender').select2({
        theme: 'bootstrap4',
        minimumResultsForSearch: Infinity,
        language: 'es',
    });

    $('#id_date_birthday').datetimepicker({
        locale: 'es',
        format: 'YYYY-MM-DD',
        useCurrent: false,
        maxDate: new Date(),
    });

    $('input[name="first_names"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });
    $('input[name="last_names"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });

    $('input[name="phone"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers');
    });
});