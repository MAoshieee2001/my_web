let customer = {
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
                    action: 'get_customers',
                }, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "position"},
                {"data": "full_names"},
                {"data": "gender.names"},
                {"data": "date_birthday"},
                {"data": "dni"},
                {"data": "address"},
                {"data": "phone"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a class="btn btn-warning btn-xs" href="' + pathname + 'update/' + data + '/"><i class="fas fa-edit"></i></a> ' +
                            '<a class="btn btn-danger btn-xs" href="' + pathname + 'delete/' + data + '/"><i class="fas fa-trash"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });

    }
}

$(function () {
    customer.list();
});