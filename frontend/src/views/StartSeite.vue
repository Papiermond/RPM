<template>
  <h1>Startseite</h1>
  <div class="button-container">
    <button @click="$router.push('/kunden')">Kunden</button>
    <button @click="$router.push('/produkte')">Produkte</button>
    <button @click="$router.push('/auftrag')">Auftrag</button>
    <button @click="$router.push('/DSGVO')">DSGVO</button>
  </div>
</template>

<style>
.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #369c6e;
}
</style>