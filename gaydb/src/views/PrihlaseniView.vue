<script>
import axios from 'axios'

export default {
    data() {
        return {
            username: "",
            password: "",
            spatneHeslo: false,
            spatnyUsername: false,
            errors: [],
            showError: false,
            prihlasen: null,
        }
    },
    mounted() {
        this.prihlasen = false
        if (localStorage.getItem("token") != null) {
            console.log("logged")
            this.prihlasen = true
        } 
    },
    methods: {
        login(e){
            e.preventDefault()
            console.log("posíláááám")
            if (this.username.length < 5){
                this.spatnyUsername = true
                this.errors.push("zadejte jméno")
            } else if (this.password.length < 5){ //nic nenapsal - snad
                this.spatneHeslo = true
            }
            //if (this.spatnyUsername || this.spatneHeslo) return //nic se nestane
            
            axios.post('/prihlaseni', {
                "username": this.username,
                "password": this.password,
            })
            .then(response => {
                //localStorage.setItem("token_type",response.data.token_type)
                localStorage.setItem("token", response.data.token)
                this.$router.push('/ucet');
            })
            .catch(error => {
                this.errors.push("Špatné uživatelské jméno nebo heslo")
                this.spatneHeslo = true
            });
        },
        prihlasitOnSuccess(){

        },
        zmena() { // pokud zacnu znova psat tak zrusim znaceni spatnyho inputu
            this.spatnyEmail = false
            this.spatneHeslo = false
        },
        checkUdaje(udaje){
            console.log("more");
            if (udaje === "heslo" && this.password !== undefined){
                this.spatneHeslo = !/^(?=.*[a-zA-Z]).{5,128}$/.test(this.password); //aspoň 5 znaků
            }
            else if(udaje === "username" && this.username.length === 0){
                this.spatnyUsername = true;
            } 
                
            console.log(this.spatneHeslo, this.spatnyUsername)
        },
    }
}

</script>

<template>
    <h1 class="nadpis">Login screen</h1>
    <div class="op">
        <div class="kontejner_login">
            <form class="login_form">
                <label class="label" for="uname">Jmeno:</label>
                <input :class="{wrong_input: spatnyUsername, text_input: !spatnyUsername}" name="uname" @:input="checkUdaje('username')"
                :oninput="zmena"  type="text" v-model="username" placeholder="Zadejte email"/>

                <label class="label" for="password">Heslo:</label>
                <input :class="{wrong_input: spatneHeslo, text_input: !spatneHeslo}" name="password" type="password" @:input="checkUdaje('heslo')" 
                :oninput="zmena" v-model="password" placeholder="Zadejte heslo"/>

                <button v-on:click="login" class="btn" type="submit">Přihlásit</button>
                <hr class="herka">
                <a href="/registrace" id="podform">Založení účtu: Registrace</a>
                <p v-for="p in errors">{{ p }}</p>
            </form>
        </div>
    </div>
</template>

<style>
p {
    display: flex;
    color: white;
    font-size: 1.2em;
    justify-content: center;
}

.wrong_input{
    border: red solid 2px;
}

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

</style>