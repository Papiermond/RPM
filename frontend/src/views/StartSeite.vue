<template>
  <div>
    <h1>Startseite</h1>
    <button @click="$router.push('/kunden')">Kunden</button>
    <button @click="$router.push('/produkte')">Produkte</button>
    <button @click="$router.push('/auftrag')">Auftrag</button>
  </div>
</template>

<style>
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 1rem;
}

button:hover {
  background-color: #369c6e;
}</style>