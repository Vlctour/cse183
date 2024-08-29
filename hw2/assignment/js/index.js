"use strict";

let app = {};


app.data = {    
    data: function() {
        return {
            // Complete.
            text: [
                "Wages, salaries, and tips. This should be shown in box 1 of your Form(s) W-2. Attach your Form(s) W-2.",
                "Taxable interest from 1099 forms.",
                "Other Income not included in 1 and 2.",
                "Add lines, 1, 2, and 3. This is your adjusted gross income",
                "If this is a joint return, add your spouse as a dependent. Write $13,850 for an individual return and $27,700 for a joint return.",
                "Subtract line 5 from line 4. If line 5 is larger than line4, enter -0-. This is your taxable income.",
                "Federal income tax withheld from Form(s) W-2 and 1099.",
                "Earned income credit (EIC).",
                "Add lines 7 and 8a. These are your total payments and credits.",
                "Tax. Use the amount on line 6 above to find your tax in the tax table in the instructions. Then, enter the tax from the table on this line.",
                "Other Taxes",
                "Add lines 10 and 11. This is your total tax.",
                "If line 9 is larger than line 12, subtract line 12 from line 9. This is your refund. If Form 8888 is attached, check here.",
                "If line 12 is larger than line 9, subtract line 9 from line 12. This is the amount you owe. For details on how to pay, see instructions."
            ],
            value: ["", "", "", 0, 13850, 0, "", "", 0, 0, "", 0, 0, 0],
            checked: false,
        };
    },
    methods: {
        // Complete.
        add: function(line) {
            let convert = null;
            // 0 indexing, we want to update row 4
            if (line == "add-income") {
                this.value[3] = Number(this.value[0]) + Number(this.value[1]) + Number(this.value[2])
                convert = 3
                this.subtract()
            } else if (line == "add-credits") {
                this.value[8] = Number(this.value[6]) + Number(this.value[7])
                convert = 8
                this.final()
            } else if (line == "add-tax") {
                this.value[11] = Number(this.value[9]) + Number(this.value[10])
                convert = 11
                this.final()
            }

            if (convert != null) {
                this.value[convert] = (Number.isInteger(this.value[convert])) ? this.value[convert] : this.value[convert].toFixed(2);
            }
            return;
        },
        subtract: function() {
            // 0 indexing
            if (Number(this.value[4]) > Number(this.value[3])) {
                this.value[5] = 0
            } else {
                this.value[5] = Number(this.value[3]) - Number(this.value[4])
                this.value[5] = (Number.isInteger(this.value[5])) ? this.value[5] : this.value[5].toFixed(2);
            }

            this.tax()
        },
        checkbox: function() {
            // 0 indexing, we want to update row 5
            if (this.checked) {
                this.value[4] = 27700
            } else {
                this.value[4] = 13850
            }
            this.subtract()
        },
        tax: function() {
            // 0 indexing, check row 6, and see how much to tax
            let is_joint = this.checked + 1, start = 0, total_tax = 0;
            var rates = [
                [10, 0, 0],
                [12, 11000, 22000],
                [22, 44725, 89450],
                [24, 95375, 190750],
                [32, 182100, 364200],
                [35, 231250, 462500],
                [37, 578125, 693750]
            ]

            // figure out the start for our summation
            for (const i in rates) {
                if (this.value[5] < rates[i][is_joint]) {
                    break;
                }
                start++;
            }
            start -= 1

            // start value must be the taxable income - the bracket it belongs to,
            // afterwards, the value has to correspond to the bracket value - the bracket it belongs to
            let curr_bracket = this.value[5]
            for (let j = start; j >= 0; j--) {
                let next_bracket = rates[j][is_joint]
                total_tax += (rates[j][0] / 100) * (curr_bracket - next_bracket)
                curr_bracket = next_bracket

            }

            this.value[9] = total_tax
            this.value[9] = (Number.isInteger(this.value[9])) ? this.value[9] : this.value[9].toFixed(2);
            this.add("add-tax");

            return;
        },
        final: function() {
            if (this.value[8] > this.value[11]) {
                this.value[12] = this.value[8] - this.value[11]
                this.value[13] = 0
            } else if (this.value[11] > this.value[8]) {
                this.value[12] = 0
                this.value[13] = this.value[11] - this.value[8]
            } else {
                this.value[12] = this.value[13] = 0
            }
            
            this.value[12] = (Number.isInteger(this.value[12])) ? this.value[12] : this.value[12].toFixed(2);
            this.value[13] = (Number.isInteger(this.value[13])) ? this.value[13] : this.value[13].toFixed(2);

            return;
        }
    }
};

app.vue = Vue.createApp(app.data).mount("#app");
app.vue.recompute();

