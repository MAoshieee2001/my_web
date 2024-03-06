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
                {"data": "position"},
                {"data": "customer.full_names_DNI"},
                {"data": "date_joined"},
                {"data": "employee.full_names"},
                {"data": "total"},
                {"data": "action.names"},
                {"data": "date_log"},
                {"data": "user_log.full_names"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-warning">S/ ' + parseFloat(data).toFixed(2) + '</span>';
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