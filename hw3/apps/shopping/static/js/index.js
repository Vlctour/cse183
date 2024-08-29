"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {
    data: function() {
        return {
            // Complete as you see fit.
            shopping_list: [],
            new_item: "",
        };
    },
    methods: {
        // Complete as you see fit.
        find_item_idx: function(id) {
            // return this.shopping_list.findIndex(item => item.id === id)
            for (let i = 0; i < this.shopping_list.length; i++) {
                if(this.shopping_list[i].id === id) {
                    return i
                }
            }
            return null
        },
        add_item: function() {
            // first insert into db
            // we need self because after the post
            // when we enter then, "this" is in regards
            // to something else
            let self = this
            axios.post(add_data_url, {
                item_name: self.new_item,
                purchased: false
            }).then(function (r) {
                // here is where we are actually updating
                // the dictionary on .js
                // console.log("response:", r)
                // prepend items
                // console.log("add", self.shopping_list)
                // console.log(typeof self.shopping_list)

                self.shopping_list.unshift({
                    id: r.data.id,
                    item_name: self.new_item,
                    purchased: false
                });
                self.new_item = ""
            });
        },
        change_item: async function(item_id) {
            await new Promise(resolve => setTimeout(resolve, 0));
            let self = this
            let i = self.find_item_idx(item_id)
            let updated_item = self.shopping_list.splice(i, 1)[0];

            if (updated_item.purchased) {
                self.shopping_list.push(updated_item);
            } else {
                self.shopping_list.unshift(updated_item);
            }
            axios.post(change_item_url, {
                id: item_id
            }).then(function (r) {
                // old implementation
                // self.shopping_list[i].purchased = r.data.purchased
                // self.shopping_list = self.shopping_list.filter(item => item.id !== item_id);

                // let updated_item = self.shopping_list.splice(i, 1)[0];
                // if (r.data.purchased) {
                //     self.shopping_list.push(updated_item);
                // } else {
                //     self.shopping_list.unshift(updated_item);
                // }

                // might not be the best approach, but easiest
                // app.load_data()
            })
        },
        delete_item: function(item_id) {
            let self = this
            let i = self.find_item_idx(item_id)
            // idk how to use axios.delete
            axios.post(delete_item_url, {
                id: item_id
            }).then(function (r) {
                self.shopping_list.splice(i, 1)
            })
        }

    },
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
    axios.get(load_data_url).then(function (r){
        // console.log("Load data status code:", r.status)
        app.vue.shopping_list = r.data.shopping_list;
    });
}

// This is the initial data load.
app.load_data();

