"use strict";

// Complete. 
let app = {};

function reset_selected(tags) {
    let new_tags_selected = []
    for (let i = 0; i < tags.length; i++) {
        new_tags_selected.push(false)
    }
    app.vue.tags_selected = new_tags_selected
}

app.data = {
    data: function() {
        return {
            posts: [],
            deletable: [],
            tags: [],
            tags_selected: [],
            tag_names_selected: [],
            new_post: "",
        };
    },
    methods: {
        find_post_idx: function(id) {
            for (let i = 0; i < this.posts.length; i++) {
                if(this.posts[i].id === id) {
                    return i
                }
            }
            return null
        },
        find_tag_idx: function(tag) {
            for (let i = 0; i < this.tags.length; i++) {
                if(this.tags[i].tag === tag) {
                    return i
                }
            }
            return null
        },
        find_tag_name_idx: function(tag) {
            for (let i = 0; i < this.tag_names_selected.length; i++) {
                if(this.tag_names_selected[i].tag === tag) {
                    return i
                }
            }
            return null
        },
        add_post: function() {
            self = this
            axios.post(add_post_url, {
                post: self.new_post
            }).then(function (r) {
                self.posts.unshift({
                    id: r.data.id,
                    user_email: r.data.user_email,
                    post: r.data.post,
                    date_time: r.data.date_time
                })
                self.deletable.unshift(1)
                self.new_post = ""
                self.update_tags(r.data.tags)
            })
        },
        update_tags: function(tags) {
            self = this
            // will be very slow but whatever i guess
            // known error, weird stuff happens if a tag
            // is selected while a deletion occurs
            // never figured out how to update tags :(
            axios.get(get_tags_url).then(function(r){
                app.vue.tags = r.data.tags
                reset_selected(app.vue.tags)
            })
        },
        filter_tag: function(tag) {
            let self = this
            let i = self.find_tag_idx(tag)
            let name_i = self.find_tag_name_idx(tag)
            self.tags_selected[i] = !self.tags_selected[i]
            if (self.tags_selected[i]) {
                self.tag_names_selected.push({tag: tag})
            } else {
                self.tag_names_selected.splice(name_i, 1)
            }

            axios.get(get_posts_url, {
                params: {len: self.tag_names_selected.length, tags: self.tag_names_selected}
            }).then(function(r){
                self.posts = r.data.posts
                let curr_user = r.data.curr_user
                for (let i = 0; i < self.posts.length; i++) {
                    if (self.posts[i].user_email == curr_user) {
                        self.deletable[i] = 1
                    } else {
                        self.deletable[i] = null
                    }
                }
            })
        },
        delete_post: function(id) {
            // note to self, error occurs when
            // tags are selected and deletion occurs
            // never figured it out :(
            self = this
            let i = self.find_post_idx(id)
            let tags = self.posts[i].tags
            self.deletable.splice(i, 1)
            self.posts.splice(i, 1)
            axios.post(delete_post_url, {
                id: id
            }).then(function (r) {
                self.update_tags({})
            })
        }
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function() {
    axios.get(get_posts_url).then(function(r){
        app.vue.posts = r.data.posts
        let curr_user = r.data.curr_user
        for (let i = 0; i < app.vue.posts.length; i++) {
            if (app.vue.posts[i].user_email == curr_user) {
                app.vue.deletable[i] = 1
            } else {
                app.vue.deletable[i] = null
            }
        }
    })
    axios.get(get_tags_url).then(function(r){
        app.vue.tags = r.data.tags
        reset_selected(app.vue.tags)
    })
}

app.load_data();