let tbtSale;

let sale = {
    list: function () {
        tbtSale = $('#data').DataTable({
            serverSide: true,
            processing: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_sales',
                }, // parametros
                dataSrc: "data"
            },
            columns: [
                {"data": "position"},
                {"data": "code_sale"},
                {"data": "customer.full_names"},
                {"data": "date_joined"},
                {"data": "employee.full_names"},
                {"data": "subtotal"},
                {"data": "iva"},
                {"data": "total"},
                {"data": "cash"},
                {"data": "change"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1, 3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2, -3, -4, -6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/ ' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a class="btn btn-primary btn-xs" rel="btnDetails"><i class="fas fa-search"></i></a> ' +
                            '<a class="btn btn-success btn-xs" href="' + pathname + 'invoice/pdf/' + data + '/" target="_blank"><i class="fas fa-file-pdf"></i></a> ' +
                            "<a class='btn btn-danger btn-xs' href='" + pathname + 'delete/' + data + "/' rel='btnDelete'><i class='fas fa-trash'></i></a>";
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
}

$(function () {
    sale.list();

    $('#data tbody').on('click', 'a[rel="btnDetails"]', function (evt) {
        let tr = tbtSale.cell($(this).closest('td,li')).index();
        let sale = tbtSale.row(tr.row).data();
        $('#details').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_details',
                    id_sale: sale.id,
                },
                dataSrc: ""
            },
            columns: [
                {"data": "product.long_names"},
                {"data": "quantity"},
                {"data": "price"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/ ' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });


        $('#myModalDetails').modal('show');
    });
});