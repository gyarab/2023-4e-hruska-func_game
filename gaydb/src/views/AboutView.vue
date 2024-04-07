<template>
  <div class="kontejner">
    <h1 class="nadpis">O nás</h1>
    <div class="items">
      <div id="studentsky-projekt">
        <h2 class="nadpisus">Základní informace</h2>
        <p class="text">
          Jde o studentský projekt naprogramovaný ve čtvrtém ročníku Gymnázia Arabská. Projekt je zaměřen na využití
          grafů v online hře.
          Projekt využívá javascript pro vykreslování objektů, respektive křivek na canvas, což je pole pixelů, které
          se mění dle zadaných vstupních dat.
        </p>
        <p class="text">
          Logika hry je jednoduchá, hráči mají za úkol trefit zelený obdélník na konci canvasu za pomocí funkční hodnoty
          jimi zvolenou matematickou funkcí.
          Aby to hráči neměli jednoduché, tak se uprostřed hrací plochy vygenerují překážky v podobě kruhů, které musí
          hráč, při svém snažení, obstřelit.
        </p>
        <img src="../assets/fkce.svg">
      </div>
      <div id="studentsky-projekt">
        <p class="text">
          Studentský projekt je zárověň maturitní prací. V projektu jsem si poprvé vyzkoušel pracovat sám na větším projektu obsahujícím databázi,
          autentifikaci přes JWT tokeny, frontend ve vue.js, použití fastApi web socketů na vzájemnou komunikaci uživatelů. 
        </p>
      </div>
    </div>

  </div>

</template>

<style>
img {
  width: 15%;

}

.items {
  display: flex;
  flex-direction: column;
  background-color: var(--login-form-bg);
  margin: 10px;
  padding: 15px;
  width: 60%;
  border-radius: 20px;
  height: 70vh;
  gap: 0.5em;
  align-items: center;
}

#studentsky-projekt {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.nadpisus {
  margin: 10px;
  font-size: 30px;
  text-align: start;
  color: var(--bila-soft)
}
</style>