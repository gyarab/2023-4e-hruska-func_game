<script>
import axios from 'axios'

export default {
    data() {
        return {
            formData: {
                email: "",
                password: "",
            },
            spatneHeslo: false,
            spatnyEmail: false,
            errors: [],
            showError: false,
        }
    },
    methods: {
        login(e){
            e.preventDefault()
            console.log(this.email, this.password)
            if (!this.email.length > 5){
                this.spatnyEmail = true
            } else if (!this.password){ //nic nenapsal - snad
                this.spatneHeslo = true
            }
            if (this.spatnyEmail || this.spatneHeslo) return //nic se nestane
            
            const { email, password } = this.formData;

            // Create FormData object
            const formData = new FormData();
            formData.append('username', this.email);
            formData.append('password', this.password);

            axios.post('http://127.0.0.1:5173/prihlaseni', formData)
            .then(response => {
                //localStorage.setItem("token_type",response.data.token_type)
                localStorage.setItem("token",response.data.access_token)
                this.$router.push('/ucet');
            })
            .catch(error => {
                console.error('Error:', error);
            });

            
        },
        zmena(){
            console.log("in zmena")
            this.spatnyEmail = false
            this.spatneHeslo = false
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
                <label class="label" for="uname">Email:</label>
                <input class="text_input" name="uname" type="text" v-model="email" placeholder="Zadejte email"/>

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