<script>
import axios from 'axios'

export default {
    data() {
        return {
            email: "",
            password: "",
            password2: "",
            spatneHeslo: null,
            spatnyEmail: null,
            errors: [],
            showError: false
        }
    },
    methods: {
        validateForm() {
            this.spatneHeslo = false
            this.spatnyEmail = false
            console.log("[where] upper validating form")
            if (!this.password || this.password !== this.password2) this.spatneHeslo = true;
            console.log("[WHERE] under password check")
            if (!this.email) this.spatnyEmail = true;
            if (this.spatneHeslo || this.spatnyEmail){
                if (this.spatnyEmail && this.email.length > 12) this.errorHandler("Jméno je moc dlouhé.(3-12 znaků)")
                else if (this.spatnyEmail && this.email.length < 3) this.errorHandler("Jméno je moc krátké.(3-12 znaků)")
                else if (this.spatnyEmail) this.errorHandler("Jméno může obsahovat jen velká a malá písmena, čísla a znaky _-+*!?")
                else if (this.spatnyEmail) this.errorHandler("Nesprávný email")
                else if (this.spatnyEmail) this.errorHandler("Heslo musí být delší než 5 znaků")
            }
            if (!this.spatneHeslo && !this.spatnyEmail){
                return true //v pořádku
            }
            return false //špatný input form
        },
        registrovat(e){
            e.preventDefault()
            if (this.validateForm()){
                console.log("posííííílááááám")
                axios.post('/registrace', {
                    "username": this.email,
                    "password": this.password,
                })
                .then(response => {
                    //localStorage.setItem("token_type",response.data.token_type)
                    this.$router.push('/prihlaseni');
                })
                .catch(error => {
                    this.errors.push("Špatné heslo")
                    this.spatneHeslo = true
                });
            }
            else{
                console.log("a znovu a budeš pllllnit")
            }


        },
        checkUdaje(udaje){
            const patternEmail = /^[a-zA-Z0-9]{5,}$/; //aspoň 5 písmen
            const patternPassword = /^(?=.*[a-zA-Z]).{5,128}$/ //aspoň 5 znaků, jedno písmeno
            if (udaje === "email" && this.email) this.spatnyEmail = !patternEmail.test(this.email)
            else if (udaje === "heslo" && this.password !== undefined) this.spatneHeslo = !patternPassword.test(this.password);
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
            <form class="login_form" v-on:submit="registrovat">
                <label class="label" for="uname">Email:</label>
                <input class="text_input" :@input="checkUdaje('email')" v-bind:class="{wrong_input: spatnyEmail, text_input: !spatnyEmail}"
                 type="text" v-model="email" placeholder="Zadejte email" name="uname"/>
                 
                <label class="label" for="password">Heslo:</label>
                <input class="text_input" :@input="checkUdaje('heslo')" v-bind:class="{wrong_input: spatneHeslo, text_input: !spatnyEmail}" name="password"
                type="password" v-model="password" placeholder="Zadejte heslo"/>

                <label class="label" for="password2">Heslo znovu:</label>
                <input class="text_input" :@input="checkUdaje('heslo')" v-bind:class="{wrong_input: spatneHeslo, text_input: !spatneHeslo}" name="password2"
                type="password" v-model="password2" placeholder="Zadejte heslo"/>
                
                <button v-on:click="registrovat" class="btn-in-registr" type="submit">Založit účet</button>
                <hr class="herka">
                <a href="/prihlaseni" id="podform">Máte účet? Přihlášení</a>
            </form>
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

.wrong_input{
    border: red solid 2px;
}

.btn-in-registr {
    color: white;
    width: 8em;
    font-size: 15px;
    padding: 5px;
    height: 2.5em;
    border-radius: 5px;
    background-color: var(--func-input-bg);
    border: none;
    cursor: pointer;
    align-self: center;
}

.btn-in-registr:hover {
    background-color: var(--btn-hover);
}
</style>