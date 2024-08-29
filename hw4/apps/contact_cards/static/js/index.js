"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

function reset_editables(contacts) {
    // console.log("resetting", contacts)
    for (let i = 0; i < contacts.length; i++) {
        contacts[i].editable_name = false;
        contacts[i].editable_aff = false;
        contacts[i].editable_desc = false;
    }
}

app.data = {    
    data: function() {
        return {
            contacts: [],
        };
    },
    methods: {
        // Complete.
        find_item_idx: function(id) {
            for (let i = 0; i < this.contacts.length; i++) {
                if(this.contacts[i].id === id) {
                    return i
                }
            }
            return null
        },
        toggle_edit: function(id, field) {
            let self = this;
            let i = self.find_item_idx(id);
            if (field == 'name') {
                self.contacts[i].editable_name = true;
            } else if (field == 'aff') {
                self.contacts[i].editable_aff = true;
            } else {
                self.contacts[i].editable_desc = true;
            }
        },
        click_figure: function (id) {
            let input = document.getElementById("file-input" + id);
            input.click();
        },
        select_file: function (event, id) {
            self = this
            let i = self.find_item_idx(id)
            // grab the file
            let input = event.target
            app.file = input.files[0]

            // display the image locally THEN store onto db
            if (app.file) {
                // we read the file.
                let reader = new FileReader();
                // once readasData finishes, this will trigger
                reader.addEventListener("load", function () {
                    // set the result to be displayed in the correct area
                    self.contacts[i].contact_image = reader.result;
                    // now store onto db
                    let file_name = app.file.name;
                    let file_type = app.file.type;
                    axios.post(file_upload_url, {
                        file_name: file_name,
                        file_type: file_type,
                        id: id,
                        contact_image: self.contacts[i].contact_image
                    }).then(function (r) {})
                    // reset global var
                    app.file = null
                });
                // read the image as a data, then reader.addevent will trigger once this
                // is done
                reader.readAsDataURL(app.file);
            }
        },
        add_contact: function() {
            self = this
            // first display the non trivial things for the contact
            self.contacts.push({
                contact_name: "",
                contact_affiliation: "",
                contact_description: "",
                contact_image: "https://bulma.io/assets/images/placeholders/96x96.png"
            })
            axios.get(add_contacts_url, {}).then(function (r){
                // then add the id and user_email as a necessity later
                let recent_contact_loc = self.contacts.length - 1
                self.contacts[recent_contact_loc]["id"] = r.data.id
                self.contacts[recent_contact_loc]["user_email"] = r.data.user_email
            })
        },
        update_contact: function(id, field) {
            self = this
            let i = self.find_item_idx(id)
            if (field == 'contact_name') {
                self.contacts[i].editable_name = false;
            } else if (field == 'contact_affiliation') {
                self.contacts[i].editable_aff = false;
            } else {
                self.contacts[i].editable_desc = false;
            }
            axios.post(update_contacts_url, {
                id: id,
                field: field,
                field_data: self.contacts[i][field]
            }).then(function(r) {})
        },
        del_contact: function(id) {
            self = this
            let i = self.find_item_idx(id)
            axios.post(del_contacts_url, {
                id: id
            }).then(function (r) {
                self.contacts.splice(i, 1)
            })
        }
    }
};

app.file = null;

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
    axios.get(get_contacts_url).then(function(r){
        // console.log(r)
        let c = r.data.contacts
        reset_editables(c)
        app.vue.contacts = c
        // for (let i = 0; i < c.length; i++) {
        //     let reader = new FileReader();
        //     reader.addEventListener("load", function () {
        //         self.contacts[i].contact_image = reader.result;
        //     });
        //     reader.readAsDataURL(app.file);
        // }

    });
}

app.load_data();

