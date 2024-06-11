let input_range;

let report_sale = {
    list: function (all) {
        let params = {
            action: 'get_sales',
            start_date: input_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            end_date: input_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        }

        if (all) {
            params['start_date'] = '';
            params['end_date'] = '';
        }

        $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat btn-xs'
                },
                {
                    extend: 'pdfHtml5',
                    text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-flat btn-xs',
                    download: 'open',
                },
                {
                    extend: 'csv',
                    text: 'Descargar Csv <i class="fas fa-file-csv"></i>',
                    className: 'btn btn-secondary btn-flat btn-xs'
                }

            ],
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: params, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "date_joined"},
                {"data": "code_sale"},
                {"data": "customer.full_names"},
                {"data": "subtotal"},
                {"data": "iva"},
                {"data": "total"},
                {"data": "cash"},
                {"data": "change"},
                {"data": "employee.full_names"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/ ' + parseFloat(data).toFixed(2);
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
            ],
            initComplete: function (settings, json) {

            }
        });


    }
}

$(function () {
    input_range = $('input[name="date_range"]');


    input_range.daterangepicker({
        autoApply: true,
        language: 'es',
        locale: {
            format: 'YYYY-MM-DD',
        }
    });

    input_range.on('apply.daterangepicker', function (ev, picker) {
        report_sale.list(false);
    });

    $('#btnShowAll').on('click', function () {
        report_sale.list(true);
    });

    report_sale.list(true);
});