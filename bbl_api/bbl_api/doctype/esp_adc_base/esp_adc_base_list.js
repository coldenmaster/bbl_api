frappe.listview_settings["Esp Adc Base"] = {
    hide_name_column: true, // hide the last column which shows the `name`
    hide_name_filter: true, // hide the default filter field for the name column
    onload(listview) {
        // console.log("list onload")
        // triggers once before the list is loaded
    },
    // before_render() {
    //     console.log("list before_render")
        // triggers before every render of list records
    // },
};
