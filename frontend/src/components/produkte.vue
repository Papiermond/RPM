<template>
  <div>
    <button @click="$router.push('/')" class="back-button">Zurück</button>
    <h2>Produkte</h2>
    <table>
        <thead>
            <tr>
                <th class="border p-2">Produkt Nr.</th>
                <th class="border p-2">Produktname</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="produkt in produkt" :key="produkt.id">
                <td class="border p-2">{{ produkt.Produkt_Nr }}</td>
                <td class="border p-2">{{ produkt.Produktname }}</td>
            </tr>
        </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ProduktListe',
  data() {
    return {
      produkt: []
    }
  },
  mounted() {
    fetch('http://localhost:5000/api/produkte')
      .then(response => response.json())
      .then(data => {
        this.produkt = data
      })
      .catch(error => {
        console.error('Fehler beim Laden der Produktdaten:', error)
      });
  }
}
</script>

<style scoped>
.back-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.back-button:hover {
  background-color: #369c6e;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  text-align: left;
}

thead {
  background-color: #5353ec;
  color: white;
}

tbody tr:nth-child(even) {
  background-color: #cbcbcb;
}

tbody tr:hover {
  background-color: #e6f7f0;
}
</style>