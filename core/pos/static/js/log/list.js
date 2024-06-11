let log = {
    list: function () {
        $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_logs',
                }, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "date_log"},
                {"data": "user_log.full_names"},
                {"data": "code_sale"},
                {"data": "customer.full_names"},
                {"data": "date_joined"},
                {"data": "total"},
                {"data": "cash"},
                {"data": "change"},
                {"data": "action"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-danger">' + data.names + '</span>';
                    }
                },
                {
                    targets: [-2, -3, -4],
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


    }
}

$(function () {
    log.list();
});