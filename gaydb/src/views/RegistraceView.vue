<script>
import axios from 'axios'

export default {
    data() {
        return {
            email: "",
            password: "",
            password2: "",
            prihlasen: false,
            spatneHeslo: false,
            spatnyEmail: false,
            errors: [],
            showError: false
        }
    },
    methods: {
        validateForm(e) {
            e.preventDefault();

            console.log("validating form")
            this.errors = [];
            if (!this.password) this.spatneHeslo = true;
            if (!this.email) this.spatnyEmail = true;

            if (this.spatneHeslo || this.spatnyEmail){
                if (this.spatnyEmail && this.jmeno.length > 12) this.errorHandler("Jméno je moc dlouhé.(3-12 znaků)")
                else if (this.spatnyEmail && this.email.length < 3) this.errorHandler("Jméno je moc krátké.(3-12 znaků)")
                else if (this.spatnyEmail) this.errorHandler("Jméno může obsahovat jen velká a malá písmena, čísla a znaky _-+*!?")
                else if (this.spatnyEmail) this.errorHandler("Nesprávný email")
                else if (this.spatnyEmail) this.errorHandler("Heslo musí být delší než 5 znaků")
                return
            }
            console.log(this.errors)
        },
        registrovat(){
            console.log(this.errors)
            this.validateForm();

        },
        checkUdaje(udaje){
            if (udaje === "email" && this.email) this.spatnyEmail = !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(this.email.value); //valid email
            else if (udaje === "heslo" && this.password !== undefined) this.spatneHeslo = !/^(?=.*[a-zA-Z]).{5,128}$/.test(this.password); //aspoň 5 znaků
            if(udaje === "email" && this.email.length === 0) this.spatnyEmail = true
            else if(udaje === "heslo" && this.password.length === 0 || this.password2.length === 0) this.spatneHeslo = true
            
        },
        errorHandler(oznameni){
            this.errors.push(oznameni)
        }
    }
}

</script>

<template>
    <h1 class="nadpis">Registrace</h1>
    <div class="op">
        <div class="kontejner_register">
            <form class="login_form" method="post" v-on:submit="registrovat">
                <label class="label" for="uname">Email:</label>
                <input class="text_input" :@input="checkUdaje('email')" v-bind:class="{ 'invalid': errors.length && !this.spatneHeslo }"
                 type="text" v-model="email" placeholder="Zadejte email" name="uname"/>
                 
                <label class="label" for="password">Heslo:</label>
                <input class="text_input" :@input="checkUdaje('heslo')" v-bind:class="{ 'invalid': errors.length && !this.spatneHeslo }"
                type="password" v-model="password" placeholder="Zadejte heslo"/>

                <label class="label" for="password2">Heslo znovu:</label>
                <input class="text_input" :@input="checkUdaje('heslo')" v-bind:class="{ 'invalid': errors.length && !this.spatneHeslo }" name="password2"
                type="password" v-model="password2" placeholder="Zadejte heslo"/>
                
                <button v-on:click="registrovat" class="btn" type="submit">Založit účet</button>
                <hr class="herka">
                <a href="/prihlaseni" id="podform">Mámte účet?: Přihlášení</a>
            </form>
        </div>
        <div v-if="this.errors">
            <p v-for="error in errors">{{ error }}</p>
        </div>
    </div>
    </template>

<style>
.kontejner_register {
    display: flex;
    flex-direction: column;
    gap: 2em;
    align-items: center;
    height: 80vh;
    width: 50%;
    padding: 10px;
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

.fade-enter-active,
.fade-leave-active {
    transition: opacity 1s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>