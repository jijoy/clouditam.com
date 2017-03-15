$(function () {
    $("#assets-data").dataTable({
        "columnDefs": [
            {"width": "12%", "targets": 10},
            {"bSortable": false, "aTargets": [10]}
        ]
    });
    $("#manufacturer-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 2},
            {"width": "30%", "targets": 1},
            {"bSortable": false, "aTargets": [1,2]}
        ]
    });
    $("#supplier-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 2},
            {"width": "30%", "targets": 6},
            {"bSortable": false, "aTargets": [5,6]}
        ]
    });
    $("#location-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 2},
            {"width": "30%", "targets": 9},
            {"bSortable": false, "aTargets": [2,3,9]}
        ]
    });
    $("#hardware-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 1},
            {"width": "15%", "targets": 3},
            {"bSortable": false, "aTargets": [3]}
        ]
    });
    $("#software-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 1},
            {"width": "15%", "targets": 7},
            {"bSortable": false, "aTargets": [1,7]}
        ]
    });
    $("#users-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "30%", "targets": 1},
            {"width": "15%", "targets": 6},
            {"bSortable": false, "aTargets": [6]}
        ]
    });
    $("#company-data").dataTable({
        "columnDefs": [
            {"width": "30%", "targets": 0},
            {"width": "15%", "targets": 1},
            {"bSortable": false, "aTargets": [1]}
        ]
    });

})