frappe.listview_settings["Elec Meter RT"] = {
    hide_name_column: true, // hide the last column which shows the `name`
    hide_name_filter: true, // hide the default filter field for the name column
	// add_fields: ["public"],
	// get_indicator: function (doc) {
	// 	if (doc.public) {
	// 		return [__("Public"), "green", "public,=,Yes"];
	// 	} else {
	// 		return [__("Private"), "gray", "public,=,No"];
	// 	}
	// },
    onload(listview) {
        // console.log("list onload")
        // triggers once before the list is loaded
    },
    before_render() {
        // console.log("list before_render")
        // triggers before every render of list records
    },
    button: {
        show(doc) {
            return doc.reference_name;
        },
        get_label() {
            return 'View';
        },
        get_description(doc) {
            return __('View {0}', [`${doc.reference_type} ${doc.reference_name}`])
        },
        action(doc) {
            frappe.set_route('Form', doc.reference_type, doc.reference_name);
        }
    },
};
