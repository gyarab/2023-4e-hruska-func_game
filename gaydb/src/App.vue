<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const prihlasen = ref(false)

const checkPrihlasen = () => {
  if (localStorage.getItem("token") !== null) {
    prihlasen.value = true
  } 
}

onMounted(() => {
  checkPrihlasen() // Check the login status when the component is mounted
})
</script>

<template>
  <header>
    <nav id="menu">
      <div id="menu-navs">
        <div class="link-kontejner">
          <RouterLink to="/">O nás</RouterLink>
        </div>
        <div class="link-kontejner">
          <RouterLink to="/play">Hrát</RouterLink>
        </div>
        <div v-if="!prihlasen" class="link-kontejner">
          <RouterLink to="/prihlaseni">Přihlášení</RouterLink>
        </div>
        <div v-else class="link-kontejner">
          <RouterLink to="/ucet">Můj účet</RouterLink>
        </div>
      </div>
      <img id="logo" src="@/assets/pear.svg"/>
    </nav>
  </header>

  <div id="view">
    <RouterView />
  </div>
</template>

<style scoped>
#menu-navs {
  display: flex;
}

.link-kontejner {
  width: 9em;
  display: flex;
  justify-content: center;
  align-items: center;
}

#view {
  display: flex;
  flex-direction: column;
}

#menu {
  display: flex;
  row-gap: 10%;
  height: var(--vyska-menu);
  user-select: none;
  justify-content: space-between;
  padding: 0 2em; 
  align-items: center;
}

#menu a {
  font-family: Inter, sans-serif;
  font-size: var(--velikost-pisma-menu);
  color: var(--seda-color);
  text-decoration: none;
  vertical-align: middle;
  line-height: var(--vyska-menu);
  transition-duration: 0.2s;
}

#menu a:hover {
  font-size: 1.3em;
  padding: 0;
  transition-duration: 0.1s;
}

#logo {
  align-self: flex;
  height: 80%;
}

@media (min-width: 1024px) {}
</style>
