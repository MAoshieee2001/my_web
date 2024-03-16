// * Funcióm que muetra un SweetAlert2
function get_sweetalert2(args) {
    if (!args.hasOwnProperty('icon')) {
        args.icon = 'success';
    }
    if (!args.hasOwnProperty('title')) {
        args.title = 'Notificación del sistema!';
    }
    if (!args.hasOwnProperty('html')) {
        args.html = '';
    }
    if (!args.hasOwnProperty('timer')) {
        args.timer = 2000;
    }

    Swal.fire({
        icon: args.icon,
        title: args.title,
        confirmButtonText: 'De acuerdo!',
        html: args.html,
        timerProgressBar: true,
        timer: args.timer,
    }).then(function () {
        args.callback();
    });
}

// * Función que me permite mostrar errores de mi servidor
function get_errors(content) {
    let errors = '';

    if (typeof (content) === 'object') {
        errors = '<ul  style="padding-left: 0; list-style-position: inside;">';
        $.each(content, function (key, value) {
            errors += '<li>' + value + '</li>';
        });
        errors += '</ul>';
    } else {
        errors = '<p>' + content + '</p>';
    }

    get_sweetalert2({
        'icon': 'error',
        'html': errors,
        'callback': function () {

        }
    });
}

// * Función que me permitira mostrar un preload antes de recibir datoa de mi servidor
function loading() {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-cog fa-spin",
    });
}

// * Función que me permitira enviar información a mi servidor
function set_data_server(args) {

    if (!args.hasOwnProperty('title')) {
        args.title = 'Notificación del sistema!';
    }

    if (!args.hasOwnProperty('content')) {
        args.content = '¿Estas seguro que deseas realizar la siguiente acción?';
    }

    $.confirm({
        icon: 'fas fa-info-circle',
        title: args.title,
        content: args.content,
        columnClass: 'medium',
        draggable: false,
        theme: 'Modern',
        buttons: {
            confirm: {
                text: 'Confirmar',
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        headers: {'X-CSRFToken': csrfToken},
                        url: pathname,
                        type: 'POST',
                        dataType: 'json',
                        data: args.params,
                        contentType: false,
                        processData: false,
                        beforeSend: function () {
                            loading();
                        },
                        success: function (response) {
                            if (!response.hasOwnProperty('error')) {
                                args.callback(response);
                                return false;
                            }
                            get_errors(response.error);
                        },
                        error: function (xhr, errorType, errorMessage) {
                            alert(errorType + ' ' + errorMessage);
                        },
                        complete: function () {
                            $.LoadingOverlay("hide");
                        }
                    });
                }
            },
            cancel: {
                text: 'Cancelar',
                btnClass: 'btn-red',
                action: function () {
                }
            },
        }
    });
}

// * Funcion que me permitira validar los campos de entrada
function validate_text_box(event, type) {
    let key = event.keyCode || event.which;
    let isBackspace = key === 8;

    switch (type) {
        case "numbers":
            return (key >= 48 && key <= 57) || isBackspace; // Números del 0 al 9
        case "numbers_spaceless":
            return (key >= 48 && key <= 57); // Números del 0 al 9 sin espacios
        case "letters":
            return ((key >= 65 && key <= 90) || (key >= 97 && key <= 122) || key === 32 || isBackspace); // Letras A-Z, a-z y espacio en blanco
        case "numbers_letters":
            return ((key >= 48 && key <= 57) || (key >= 65 && key <= 90) || (key >= 97 && key <= 122) || isBackspace); // Números y letras
        case "letters_spaceless":
            return ((key >= 65 && key <= 90) || (key >= 97 && key <= 122)); // Letras A-Z y a-z sin espacios
        case "decimals":
            return ((key >= 48 && key <= 57) || isBackspace || key === 46); // Números del 0 al 9 y punto decimal
        default:
            return true;
    }
}

// * Funcion que me permitira mostrar un confirmar para un acción en especifico
function get_dialog_confirm(args) {

    if (!args.hasOwnProperty('title')) {
        args.title = 'Notificación del sistema!';
    }

    if (!args.hasOwnProperty('content')) {
        args.content = '¿Estas seguro que deseas realizar la siguiente acción?';
    }

    $.confirm({
        icon: 'fas fa-info-circle',
        title: args.title,
        content: args.content,
        columnClass: 'medium',
        draggable: false,
        theme: 'Modern',
        buttons: {
            confirm: {
                text: 'Confirmar',
                btnClass: 'btn-success',
                action: function () {
                    args.success();
                }
            },
            cancel: {
                text: 'Cancelar',
                btnClass: 'btn-red',
                action: function () {
                    args.cancel();
                }
            },
        }
    });
}

