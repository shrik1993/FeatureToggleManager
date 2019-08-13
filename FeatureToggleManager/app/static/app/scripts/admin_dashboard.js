function datatotable_gen(data, table_id, token) {
    const keys = Object.keys(data['data'][0]);
    // Create coloumn headings dynamically from the input data.
    var columns = [];
    $.each(keys, function (i, v) {
        columns.push({ 'data': v, 'title': v });
    });

    myTables = $("#" + table_id).DataTable({
        "data": data['data'],
        "columns": columns,
        dom: 'Bfrtip',        // Needs button container
        select: 'single',
        //responsive: true,
        altEditor: true,
        buttons: [{
            text: 'Add',
            name: 'add'        // do not change name
        },
        {
            extends: 'selected',
            text: 'Edit',
            name: 'edit'        // do not change name
        },
        {
            extends: 'selected',
            text: 'Delete',
            name: 'delete'        // do not change name
        },
        'copy', 'excel', 'pdf', 'colvis',
        ],
        onAddRow: function (datatable, rowdata, success, error) {
            console.log(rowdata);
            $.ajax({
                url: '/table/admin_table/',
                headers: { "X-CSRFToken": token },
                type: 'POST',
                data: rowdata,
                success: function (data) {
                    alert(data); 
                },
                error: function (data) {
                    alert(data);
                },
            });
        },
    });
};