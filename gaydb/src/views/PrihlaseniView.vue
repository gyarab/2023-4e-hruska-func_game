<script>
export default {
    data() {
        return {
            email: null,
            password: null,
            errors: [],
            showError: false
        }
    },
    methods: {
        validateForm(e) {
            console.log("validating form")
            this.errors = [];
            if (!this.password) {
                this.errors.push("Name required.");
                console.log("password required")
            }
            if (!this.email) {
                console.log("empty email")
                this.errors.push('Email required.');
            } else if (!this.validEmail(this.email)) {
                console.log("invalid email")
                this.errors.push('Valid email required.');
            }
            if (!this.errors.length) {
                return true;
            }
            e.preventDefault();

            this.showError = true;
            setTimeout(() => {
                this.showError = false;
            }, 2000);
        },
        validEmail(email) {
            let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
    }
}

</script>

<template>
    <h1 class="nadpis">Login screen</h1>
    <div class="op">
        <div class="kontejner_login">
            <form class="login_form" method="post" v-on:submit="validateForm">
                <label class="label" for="uname">Email:</label>
                <input class="text_input" v-bind:class="{ 'invalid': errors.length && !validEmail(email) }" name="uname"
                type="text" v-model="email" placeholder="Zadejte email" required />
                <label class="label" for="password">Heslo:</label>
                <input class="text_input" v-bind:class="{ 'invalid': errors.length && !password }" name="password"
                type="password" v-model="password" placeholder="Zadejte heslo" required />
                <button v-on:click="validateForm" class="btn" type="submit">Přihlásit</button>
                <hr class="herka">
                <a href="/registrace" id="podform">Založení účtu: Registrace</a>
            </form>
        </div>
        <transition name="fade">
            <div v-if="errors.length && showError" class="error_kontejner">
                <p v-for="error in errors">{{ error }}</p>
            </div>
        </transition>
    </div>
</template>

<style>
.kontejner_login {
    display: flex;
    flex-direction: column;
    gap: 2em;
    align-items: center;
    height: 70vh;
    width: 50%;
    padding: 20px;
}

#podform {
    display: flex;
    align-self: center;
    text-decoration: none;
    color: white;
    font-size: 1.2em;
}

input.invalid {
    border: 1px solid red;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 1s;
}

.fade-enter, .fade-leave-to {
    opacity: 0;
}
</style>