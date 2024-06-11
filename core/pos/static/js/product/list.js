let product = {
    list: function () {
        $('#data').DataTable({
            serverSide: true,
            processing: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_products',
                }, // parametros
                dataSrc: 'products'
            },
            columns: [
                {"data": "position"},
                {"data": "imagen"},
                {"data": "code"},
                {"data": "category.names"},
                {"data": "names"},
                {"data": "description"},
                {"data": "is_service"},
                {"data": "purchase"},
                {"data": "pvp"},
                {"data": "stock"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img class="img img-thumbnail" src="' + data + '" style="width: 50px; height: 45px;">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return (data) ? '<span class="badge badge-info">SI</span>' : '<span class="badge badge-secondary">NO</span>';
                    }
                },
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/.' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.is_service) {
                            return '-----';
                        }
                        return (data > 0) ? '<span class="badge badge-success">' + data + '</span>' : '<span class="badge badge-danger">' + data + '</span>';

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
    product.list();
});