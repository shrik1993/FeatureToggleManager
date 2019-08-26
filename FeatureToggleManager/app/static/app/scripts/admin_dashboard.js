function datatotable_gen(cols, data, table_id, token, editable, in_buttons=[]) {
    //console.log(data);
    const keys = Object.keys(data[0]);
    // Create coloumn headings dynamically from the input data.
    var columns = [];
    $.each(cols, function (i, v) {
        columns.push({'title': v });
    });
    Dt_table = $("#" + table_id).DataTable({
        "data": data ,
        "columns": columns,
        dom: 'Blfrtip',        // Needs button container
        select: 'single',
        fixedHeader: true,
        //responsive: true,
        altEditor: editable,
        buttons: in_buttons,
        onAddRow: function (datatable, rowdata, success, error) {
            rowdata["table_name"] = table_id;
            $.ajax({
                url: '/edittable/',
                headers: { "X-CSRFToken": token },
                type: 'POST',
                data: rowdata,
                success: success,
                error: error
            });
        },
        onDeleteRow: function (datatable, rowdata, success, error) {
            console.log(rowdata);
            var data = { "table_name": table_id, "index_id": rowdata['index'] };
            $.ajax({
                url: '/edittable/',
                headers: { "X-CSRFToken": token },
                type: 'DELETE',
                data: data,
                success: success,
                error: error
            });
        },
        onEditRow: function (datatable, rowdata, success, error) {
            rowdata["table_name"] = table_id;
            $.ajax({
                url: '/edittable/',
                headers: { "X-CSRFToken": token },
                type: 'PUT',
                data: rowdata,
                success: success,
                error: error
            });
        },
    });
    return Dt_table
};