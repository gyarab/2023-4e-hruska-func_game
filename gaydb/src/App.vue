<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/pear.svg" width="125" height="125" />
    <nav id="menu">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/graf">Graf</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>

#menu {
  height: var(--vyska-menu);
  padding: 0 15px;
  display: flex;
  user-select: none;
}

#menu a {
  font-family: Inter, sans-serif;
  font-size: var(--velikost-pisma-menu);
  color: var(--seda-color);
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  line-height: var(--vyska-menu);
  padding: 0 15px;
  z-index: 10;
  transition-duration: 0.2s;
}

#menu a:hover {
  font-size: 1.31em;
  padding: 0 11px;
  transition-duration: 0.2s;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 0 0 0;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
