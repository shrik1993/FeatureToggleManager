function datatotable_gen(data, table_id) {
    const keys = Object.keys(data['data'][0]);
    // Create coloumn headings dynamically from the input data.
    var columns = [];
    var fields = [];
    $.each(keys, function (i, v) {
        columns.push({ 'data': v });
        if (v.toLowerCase().includes('date')) {
            fields.push({
                'name': v,
                'label': v,
                'type': "datetime"
            });
        }
        else {
            fields.push({
                'name': v,
                'label': v
            });
        }
        $("#" + table_id + "> thead tr").append("<th>" + v + "</th>");
    });
    console.log(fields);
    console.log(data['data']);
    console.log(columns);

    $("#" + table_id).DataTable({
        "data": data['data'],
        "columns": columns,
        //buttons: [
        //    { extend: "create", editor: editor },
        //    { extend: "edit", editor: editor },
        //    { extend: "remove", editor: editor }
        //]
    });
};