let product = {
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
                    action: 'get_products',
                }, // parametros
                dataSrc: ""
            },
            columns: [
                {"data": "position"},
                {"data": "imagen"},
                {"data": "code"},
                {"data": "category.names"},
                {"data": "names"},
                {"data": "description"},
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
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-warning"> S/. ' + parseFloat(data).toFixed(2) + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
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