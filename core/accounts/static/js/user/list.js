let user = {
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
                    action: 'get_users',
                }, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "position"},
                {"data": "imagen"},
                {"data": "full_names"},
                {"data": "username"},
                {"data": "email"},
                {"data": "date_joined"},
                {"data": "groups"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img class="img img-thumbnail" src="' + data + '" style="width: 50px; height: 50px;"></img>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let html = '';
                        $.each(data, function (key, value) {
                            html += '<span class="badge badge-success">' + value.names + '</span> ';
                        });
                        return html;
                    }
                },
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
    user.list();
});