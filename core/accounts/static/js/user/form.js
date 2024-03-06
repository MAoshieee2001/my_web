$(function () {
    $('#id_groups').select2({
        placeholder: 'Seleccione un grupo de permisos.',
        theme: 'bootstrap4',
        language: 'es',
    });

    $('input[name="first_name"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });
    $('input[name="last_name"]').on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });
});