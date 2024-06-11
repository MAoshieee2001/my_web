let panel = {
    graph_pie: function () {
        $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            url: pathname,
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'get_graph_donut',
            },
            success: function (response) {
                if (!response.hasOwnProperty('error')) {
                    Highcharts.chart('container-donut', {
                        chart: {
                            type: 'pie'
                        },
                        title: {
                            text: 'Cantidad de ganancia en ventas por productos.'
                        },
                        tooltip: {
                            valueSuffix: ' nuevos soles.'
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: true,
                                    distance: 20,
                                    format: '{point.name}: {point.percentage:.1f}%'
                                }
                            }
                        },
                        series: [
                            {
                                name: 'Cantidad',
                                colorByPoint: true,
                                data: response,
                            }
                        ]
                    });

                    return false;
                }
                get_errors(response.error);
            },
            error: function (xhr, errorType, errorMessage) {
                get_errors(errorType + ' ' + errorMessage);
            },
            complete: function () {

            }
        });
    },

    graph_bar: function () {
        $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            url: pathname,
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'get_graph_bar',
            },
            success: function (response) {
                if (!response.hasOwnProperty('error')) {
                    Highcharts.chart('container-bar', {
                        chart: {
                            type: 'column'
                        },
                        title: {
                            text: 'Total de ventas por meses durante el año ' + new Date().getFullYear(),
                            align: 'center'
                        },
                        xAxis: {
                            categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                            crosshair: true,
                            accessibility: {
                                description: 'Total'
                            }
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: 'Ganancias en nuevos soles.'
                            }
                        },
                        tooltip: {
                            valueSuffix: ' nuevos soles.'
                        },
                        plotOptions: {
                            column: {
                                pointPadding: 0.2,
                                borderWidth: 0
                            }
                        },
                        series: [
                            {
                                name: 'Meses',
                                data: response
                            }
                        ]
                    });
                    return false;
                }
                get_errors(response.error);
            },
            error: function (xhr, errorType, errorMessage) {
                get_errors(errorType + ' ' + errorMessage);
            },
            complete: function () {

            }
        });
    }

}

$(function () {
    panel.graph_pie();

    panel.graph_bar();

});