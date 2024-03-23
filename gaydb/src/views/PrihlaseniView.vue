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
        }
    },
    methods: {
        login(e){
            console.log("posíláááám")
            e.preventDefault()
            console.log(this.username, this.password)
            if (!this.username.length > 5){
                this.spatnyUsername = true
            } else if (!this.password){ //nic nenapsal - snad
                this.spatneHeslo = true
            }
            if (this.spatnyUsername || this.spatneHeslo) return //nic se nestane
            
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
                console.log("spatne heslo??")
                //console.log('Error:', error);
                this.errors.push("Špatné heslo")
            });

            
        },
        zmena(){
            console.log("in zmena")
            this.spatnyUsername = false
            this.spatneHeslo = false
        },
        prihlasitOnSuccess(){

        },
        checkUdaje(udaje){
            if (udaje === "email" && this.usernameme) this.spatnyEmail = !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(this.username); //valid email
            else if (udaje === "heslo" && this.password !== undefined) this.spatneHeslo = !/^(?=.*[a-zA-Z]).{5,128}$/.test(this.password); //aspoň 5 znaků
            if(udaje === "email" && this.username.length === 0) this.spatnyEmail = true
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
                <input :class="{wrong_input: spatnyUsername, text_input: !spatnyUsername}" name="uname" @:input="checkUdaje('email')"
                 type="text" v-model="username" placeholder="Zadejte email"/>

                <label class="label" for="password">Heslo:</label>
                <input :class="{wrong_input: spatneHeslo, text_input: !spatnyUsername}" name="password" type="password" @:input="checkUdaje('email')" 
                 v-model="password" placeholder="Zadejte heslo"/>

                <button v-on:click="login" class="btn" type="submit">Přihlásit</button>
                <hr class="herka">
                <a href="/registrace" id="podform">Založení účtu: Registrace</a>
            </form>
        </div>
    </div>
</template>

<style>
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