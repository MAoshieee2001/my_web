let select_customer, txt_product, txt_iva, txt_total, txt_cash, tbtDetails, tbtProducts;
let input_dni, input_phone, input_date, input_first, input_last, select_gender;

let sale = {
    items: {
        customer: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_calculado: 0.00,
        total: 0.00,
        cash: 0.00,
        change: 0.00,
        products: []
    },
    add_detail: function (item) {
        this.items.products.push(item);
        this.list();
    },
    get_products_id: function () {
        return this.items.products.map(value => value.id);
    },
    calcule_invoice: function () {
        let iva = txt_iva.val();
        let subtotal = 0.00;

        $.each(this.items.products, function (key, value) {
            value.subtotal = value.cant * value.pvp;
            subtotal += value.subtotal;
        });

        this.items.subtotal = subtotal;
        this.items.iva = iva;
        this.items.iva_calculado = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva_calculado;

        $('input[name="subtotal"]').val(parseFloat(this.items.subtotal).toFixed(2));
        $('input[name="iva_calculado"]').val(parseFloat(this.items.iva_calculado).toFixed(2));
        $('input[name="total"]').val(parseFloat(this.items.total).toFixed(2));

        let cash = parseFloat(txt_cash.val());
        let change = cash - this.items.total;
        $('input[name="change"]').val(change.toFixed(2));

        this.items.cash = cash;
        this.items.change = change;

    },
    list: function () {
        this.calcule_invoice();
        tbtDetails = $('#details').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: sale.items.products,
            pageLength: 5,
            lengthChange: false,
            columns: [
                {"data": "id"},
                {"data": "short_names"},
                {"data": "stock"},
                {"data": "cant"},
                {"data": "pvp"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a class="btn btn-danger btn-xs" rel="drop"><i class="fas fa-trash"></i></a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" value="' + data + '" placeholder="Stock." required class="input-sm">';
                    }
                },
                {
                    targets: [-2, -1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                let tr = $(row).closest('tr');
                tr.find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                }).on('keypress', function (evt) {
                    return validate_text_box(evt, 'numbers_spaceless');
                });
            },
            initComplete: function (settings, json) {

            }
        });
    }
}


function get_resource(repo) {
    if (repo.loading) {
        return repo.text;
    }

    return $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.names + '<br>' +
        '<b>Categoría:</b> ' + repo.category.names + '<br>' +
        '<b>STOCK:</b> <span class="badge badge-success"> ' + repo.stock + '</span>' + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');
}

$(function () {
    txt_product = $('input[name="producto"]');
    txt_iva = $('input[name="iva"]');
    txt_cash = $('input[name="cash"]');
    txt_total = $('input[name="total"]');
    select_customer = $('#id_customer');

    input_dni = $('input[name="dni"]');
    input_date = $('#id_date_birthday');
    input_phone = $('input[name="phone"]');
    input_first = $('input[name="first_names"]');
    input_last = $('input[name="last_names"]');
    select_gender = $('#id_gender');


    // * -----------------Cargamos nuestros plugins
    select_customer.select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Ingrese el nombre o documento del cliente.',
        ajax: {
            headers: {'X-CSRFToken': csrfToken},
            url: pathname,
            type: 'POST',
            dataType: 'json',
            data: function (params) {
                return {
                    term: params.term,
                    action: 'get_cutomers_select2',
                };
            },
            processResults: function (data, params) {
                return {
                    results: data,
                };
            },
            cache: true,
        }
    });

    txt_product.autocomplete({
        minLength: 0,
        source: function (request, response) {
            $.ajax({
                headers: {'X-CSRFToken': csrfToken},
                url: pathname,
                type: 'POST',
                dataType: 'json',
                data: {
                    action: 'get_products_autocomplete',
                    term: request.term,
                    products_id: JSON.stringify(sale.get_products_id()),
                },
                success: function (data) {
                    response(data);
                }
            })
        },
        select: function (event, ui) {
            event.preventDefault();
            product = ui.item;
            product.cant = 1;
            product.subtotal = 0.00;
            sale.add_detail(product);
            txt_product.val('').blur();
        }
    }).focus(function () {
        $(this).autocomplete('search', $(this).val());
    });

    txt_product.data("ui-autocomplete")._renderItem = function (ul, item) {
        let listItem = $("<li>");
        if (item.imagen) {
            listItem.append('<div class="wrapper container">' +
                '<div class="row">' +
                '<div class="col-lg-2 col-sm-2">' +
                '<img src="' + item.imagen + '" class="img-fluid" style="width: 100px; height: 100px;">' +
                '</div>' +
                '<div class="col-lg-10  col-sm-10 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Categoria:</b> ' + item.category.names + '<br>' +
                '<b>Nombre:</b> ' + item.names + '<br>' +
                '<b>Stock:</b> <span class="badge badge-success">' + item.stock + '</span>' + '<br>' +
                '<b>PVP:</b> <span class="badge badge-warning">$' + item.pvp + '</span>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        }
        return listItem.appendTo(ul);
    };

    select_gender.select2({
        theme: 'bootstrap4',
        minimumResultsForSearch: Infinity,
        language: 'es',
    });

    txt_iva.TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        postfix: '%'
    }).val(0.18);

    txt_cash.TouchSpin({
        min: 0,
        max: 10000000000,
        step: 0.10,
        decimals: 2,
    }).on('keypress', function (evt) {
        return validate_text_box(evt, 'decimals');
    }).on('change', function () {
        sale.calcule_invoice();
    });

    input_date.datetimepicker({
        locale: 'es',
        format: 'YYYY-MM-DD',
        useCurrent: false,
        maxDate: new Date(),
    });

    input_first.on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });
    input_last.on('keypress', function (evt) {
        return validate_text_box(evt, 'letters');
    });

    input_phone.on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers');
    });
    input_dni.on('keypress', function (evt) {
        return validate_text_box(evt, 'numbers');
    });

    $('#details tbody').on('change', 'input[name="cantidad"]', function (evt) {
        let tr = tbtDetails.cell($(this).closest('td')).index();
        sale.items.products[tr.row].cant = parseInt($(this).val());
        sale.calcule_invoice();
        $('td:last', tbtDetails.row(tr.row).node()).html(parseFloat(sale.items.products[tr.row].subtotal).toFixed(2));
    })
        .on('click', 'a[rel="drop"]', function (evt) {
            let tr = tbtDetails.cell($(this).closest('td')).index();
            sale.items.products.splice(tr.row, 1);
            tbtDetails.row(tr.row).remove().draw();
            sale.calcule_invoice();
        });

    // * ------------------------------------------
    // Abrir el formulario de nuevo Cliente
    $('a[rel="nuevoCliente"]').on('click', function (evt) {
        $('#myModalCliente').modal('show');
    });

    $('#myModalCliente').on('hidden.bs.modal', function (event) {
        $('#frmCliente').trigger('reset');
    });

    $('#btnListadoProducto').on('click', function (evt) {
        tbtProducts = $('#products').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            lengthChange: false,
            pageLength: 5,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_products_data',
                    products_id: JSON.stringify(sale.get_products_id()),
                }, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "imagen"},
                {"data": "long_names"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img class="img-fluid" src="' + data + '" style="width: 50px; height: 50px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/.' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a class="btn btn-info btn-xs" id="btnAgregar"><i class="fas fa-plus"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalProducto').modal('show');
    });

    $('#products tbody').on('click', '#btnAgregar', function () {
        let tr = tbtProducts.cell($(this).closest('td')).index();
        let product = tbtProducts.row(tr.row).data();
        product.cant = 1;
        product.subtotal = 0.00;
        sale.add_detail(product);
        tbtProducts.row(tr.row).remove().draw();
    });

    $('#btnLimpiar').click(function () {
        txt_product.val('');
    });

    $('#btnEliminarTodo').click(function () {
        if (sale.items.products.length === 0)
            return false;

        get_dialog_confirm({
            'content': '¿Estas seguro que deseas eliminar todo el detalle de venta?',
            'success': function () {
                sale.items.products = [];
                sale.list();
            },
            'cancel': function () {

            }
        });
    });

    sale.list();

    // * -----------------Manejo de mis formularios
    $('#frmCliente').on('submit', function (evt) {
        evt.preventDefault();
        let params = new FormData(this);
        params.append('action', 'create_customer');
        set_data_server({
            'params': params,
            'callback': function (response) {
                get_sweetalert2({
                    'html': 'Se realizo correctamente la acción',
                    'callback': function () {
                        select_customer.append(new Option(response.full_names_DNI, response.id, false, true)).trigger('change');
                        $('#myModalCliente').modal('hide');
                    }
                })
            }
        });
    });

    $('#frmSale').on('submit', function (evt) {
        evt.preventDefault();

        if (sale.items.products.length === 0) {
            get_errors('Tiene que haber minimo 1 producto en el detalle de venta.');
            return false;
        }
        if (parseFloat(txt_cash.val()) < parseFloat(txt_total.val())) {
            txt_cash.focus();
            get_errors('El efectivo debe ser igual o mayor al total.');
            return false;
        }

        let params = new FormData(this);
        let data_url = $(this).attr('data-url');
        params.append('products', JSON.stringify(sale.items.products));
        set_data_server({
            params: params,
            callback: function () {
                get_dialog_confirm({
                    'content': '¿Quieres imprimir la boleta de venta?',
                    'success': function () {

                    },
                    'cancel': function () {
                        location.href = data_url;
                    }
                });
            }
        });
    });

});