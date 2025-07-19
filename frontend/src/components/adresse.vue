<template>
  <div>
    <h2>Kundenliste</h2>
    <table v-if="kunden.length">
      <thead>
        <tr>
          <th v-for="(value, key) in kunden[0]" :key="key">{{ key }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="kunde in kunden" :key="kunde.id">
          <td v-for="(value, key) in kunde" :key="key">{{ value }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Keine Kundendaten gefunden.</p>
  </div>
</template>

<script>
export default {
  name: 'KundenListe',
  data() {
    return {
      kunden: []
    }
  },
  mounted() {
    fetch('http://localhost:5000/api/adresse')
      .then(response => response.json())
      .then(data => {
        this.kunden = data
      })
      .catch(error => {
        console.error('Fehler beim Laden der Adressen:', error)
      });
  }
}
</script>
