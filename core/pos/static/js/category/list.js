let category = {
    list: function () {
        $('#data').DataTable({
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
                    action: 'get_categories',
                }, // parametros
                dataSrc: "data"
            },
            columns: [
                {"data": "position"},
                {"data": "names"},
                {"data": "description"},
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
    category.list();
});