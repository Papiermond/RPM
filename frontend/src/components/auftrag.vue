<template>
  <div>
    <button @click="$router.push('/')" class="zurueck-button">Zurück</button>
    <h2>Aufträge</h2>
    <table class="auftragstabelle">
      <thead>
        <tr>
          <th class="border p-2">Auftrag Nr</th>
          <th class="border p-2">Kunden Nr</th>
          <th class="border p-2">Datum</th>
          <th class="border p-2">Gesamtpreis</th>
          <th class="border p-2">Produkte anzeigen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="auftrag in auftraege" :key="auftrag.auftrag_Nr">
          <td class="border p-2">{{ auftrag.Auftrag_Nr }}</td>
          <td class="border p-2">{{ auftrag.kunden_Nr }}</td>  
          <td class="border p-2">{{ auftrag.Datum }}</td>
          <td class="border p-2">{{ auftrag.Gesamtpreis }}</td>
          <td class="border p-2">
            <details>
              <summary>Produkte anzeigen</summary>
              <table class="produkttabelle">
                <thead>
                    <tr>
                    <th class="border p-2">Produkt Nr.</th>
                    <th class="border p-2">Produktname</th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="produkt in auftrag.produkte" :key="produkt.produkt_Nr">
                    <td class="border p-2">{{ produkt.Produkt_Nr }}</td>
                     <td class="border p-2">{{ produkt.Produktname }}</td>
                </tr>
                </tbody>
              </table>
            </details>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'AuftragsListe',
  data() {
    return {
      auftraege: [],
      expanded: []
    };
  },
  mounted() {
    fetch('http://localhost:5000/api/auftraege')
      .then(res => res.json())
      .then(data => this.auftraege = data);
  },
  methods: {
    toggleDetails(nr) {
      if (this.expanded.includes(nr)) {
        this.expanded = this.expanded.filter(n => n !== nr);
      } else {
        this.expanded.push(nr);
      }
    }
  }
}
</script>

<style scoped>
.zurueck-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.zurueck-button:hover {
  background-color: #369c6e;
}

.auftragstabelle {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.auftragstabelle th,
.auftragstabelle td {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  text-align: left;
}

.auftragstabelle thead {
  background-color: #5353ec;
  color: white;
}

.auftragstabelle tbody tr:nth-child(even) {
  background-color: #cbcbcb;
}

.auftragstabelle tbody tr:hover {
  background-color: #e6f7f0;
}

.produkttabelle {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}

.produkttabelle th,
.produkttabelle td {
  padding: 0.5rem 1rem;
  border: 1px solid hsl(0, 0%, 0%);
  text-align: left;
}

.produkttabelle thead {
  background-color: #3d9970;
  color: #ffffff;
}

.produkttabelle tbody tr:nth-child(even) {
  background-color: hsl(219, 94%, 86%);
}

.produkttabelle tbody tr:nth-child(odd) {
  background-color: hsl(236, 93%, 84%);
}

.produkttabelle tbody tr:hover {
  background-color: hsl(184, 82%, 63%);
}
</style>
