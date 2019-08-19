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

    for (const [key, value] of Object.entries(t_data)) {
        var team_name = key.replace(/ /g, "_");
        generate_team_accordian(team_name);
        var table_name = team_name + "_table";
        if (editable) {
            datatotable_gen(value, table_name, csrf_token, editable, buttons);
        } else {
            datatotable_gen(value, table_name, csrf_token, editable)
        }
    }
}