//function add_colum_filter(table_id, d_table) {
//    // Setup - add a text input to each footer cell
//    $('#' + table_id + ' thead tr').clone(true).appendTo('#' + table_id + ' thead');
//    $('#' + table_id + ' thead tr:eq(1) tr').each(function (i) {
//        var title = $(this).text();
//        $(this).html('<input type="text" placeholder="Search ' + title + '" />');

//        $('input', this).on('keyup change', function () {
//            if (d_table.column(i).search() !== this.value) {
//                d_table
//                    .column(i)
//                    .search(this.value)
//                    .draw();
//            }
//        });
//    });
//};

function generate_datatables(t_data, csrf_token, editable) {
    buttons = [{
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
    {
        text: "Refresh",
        name: 'refresh'
    },
        'copy', 'excel', 'pdf', 'colvis',
    {
        text: 'Save Data',
        className: 'save_button',
    }
    ];
    for (var i = 0, l = t_data.length; i < l; i++) {
        var team = t_data[i]['team_name'];
        var cols = t_data[i]['columns'];
        data = t_data[i]['data'];
        var team_name = team.replace(/ /g, "_");
        generate_team_accordian(team_name);
        var table_name = team_name + "_table";
        if (editable) {
            dt_table = datatotable_gen(cols, data, team, table_name, csrf_token, editable, buttons);
        } else {
            dt_table = datatotable_gen(cols, data, team, table_name, csrf_token, editable)
        }
    }
    //for (const [key, value] of Object.entries(t_data)) {
    //    console.log(key, value);
    //    var team_name = key.replace(/ /g, "_");
    //    generate_team_accordian(team_name);
    //    var table_name = team_name + "_table";
    //    if (editable) {
    //        dt_table = datatotable_gen(value, table_name, csrf_token, editable, buttons);
    //    } else {
    //        dt_table = datatotable_gen(value, table_name, csrf_token, editable)
    //    }
    //    //add_colum_filter(table_name, dt_table);
    //}
};
