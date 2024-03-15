<script>
import axios from 'axios'

export default {
    data() {
        return {
            username: "",
            password: "",
            spatnePassword: false,
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
                this.spatnePassword = true
            }
            if (this.spatnyUsername || this.spatnePassword) return //nic se nestane
            
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
                console.log('Error:', error);
            });

            
        },
        zmena(){
            console.log("in zmena")
            this.spatnyUsername = false
            this.spatnePassword = false
        },
        prihlasitOnSuccess(){

        }
    }
}

</script>

<template>
    <h1 class="nadpis">Login screen</h1>
    <div class="op">
        <div class="kontejner_login">
            <form class="login_form">
                <label class="label" for="uname">Jmeno:</label>
                <input class="text_input" name="uname" type="text" v-model="username" placeholder="Zadejte email"/>

                <label class="label" for="password">Heslo:</label>
                <input class="text_input" name="password" type="password" v-model="password" placeholder="Zadejte heslo"/>

                <button v-on:click="login" class="btn" type="submit">Přihlásit</button>
                <hr class="herka">
                <a href="/registrace" id="podform">Založení účtu: Registrace</a>
            </form>
        </div>
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

</style>