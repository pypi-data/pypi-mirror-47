
const OnceButton = {

    template: [
        '<b-button',
        ':type="type"',
        ':native-type="nativeType"',
        ':tag="tag"',
        ':href="href"',
        ':title="title"',
        ':disabled="disabled"',
        '@click="clicked"',
        '>',
        '{{ text }}',
        '</b-button>'
    ].join(' '),

    props: {
        type: String,
        nativeType: String,
        tag: String,
        href: String,
        text: String,
        title: String,
        working: String,
        workingText: String,
        disabled: Boolean
    },

    methods: {

        clicked(event) {
            this.disabled = true
            if (this.workingText) {
                this.text = this.workingText
            } else if (this.working) {
                this.text = this.working + ", please wait..."
            } else {
                this.text = "Working, please wait..."
            }
        }
    }

}

Vue.component('once-button', OnceButton)
