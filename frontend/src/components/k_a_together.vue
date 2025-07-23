<template>
  <div>

    <button @click="$router.push('/')" class="back-button">Startseite</button>
    <h2>Kunden Daten</h2>
        <form @submit.prevent="get_KundenNr" class="form-row">
            <input v-model="vorname" placeholder="Vorname" class="input" />
            <input v-model="nachname" placeholder="Nachname" class="input" />
            <button type="submit" class="btn">Kunde suchen</button>
        </form>
        <div v-if="kundenNr">
            <strong>Kunden-Nr:</strong> {{ kundenNr }}
        </div>

        <form @submit.prevent="get_StAndOrt" class="form-row">
            <input v-model="stra_e" placeholder="Straße" class="input" />
            <input v-model="ort" placeholder="Ort" class="input" />
            <button type="submit" class="btn">Adresse prüfen</button>
        </form>
            <div v-if="anzahl !== null">
            <strong>Anzahl Kunden:</strong> {{ anzahl }}
            </div>

        <div class="form-row">
        <button @click="ort_max" class="btn">Ort mit den meisten Kunden</button>
            <div v-if="ort_name_max">
                <strong>{{ ort_name_max }}</strong> ({{ anzahl_ort }} Kunden)
            </div>
        </div>
 
    <table>
        <thead>
            <tr>
                <th class="border p-2">Kunden Nr.</th>
                <th class="border p-2">Vorname</th>
                <th class="border p-2">Nachname</th>
                <th class="border p-2">Sraße</th>
                <th class="border p-2">Haus Nr.</th>
                <th class="border p-2">PLZ</th>
                <th class="border p-2">Ort</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="kunde in kunden" :key="kunde.Kunden_Nr">
                <td class="border p-2">{{ kunde.Kunden_Nr }}</td>
                <td class="border p-2">{{ kunde.vorname }}</td>
                <td class="border p-2">{{ kunde.nachname }}</td>
                <td class="border p-2">{{ kunde.stra_e }}</td>
                <td class="border p-2">{{ kunde.Haus_Nr }}</td>
                <td class="border p-2">{{ kunde.plz }}</td>
                <td class="border p-2">{{ kunde.ort }}</td>
            </tr>
        </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'k_a_together',
  data() {
    return {
      kunden: [],
      vorname: '',
      nachname: '',
      kundenNr: null,
      fehlermeldung: '',
      stra_e: '',
      ort: '',
      ort_name_max: '',
      anzahl: null
    };
  },
  mounted() {
    fetch('http://localhost:5000/api/kunde_with_adresse')
      .then(res => res.json())
      .then(data => { this.kunden = data });
  },
  methods: {
    async get_KundenNr() {
      this.kundenNr = null;
      this.fehlermeldung = '';
      try {
        const res = await fetch('http://localhost:5000/api/get_KundenNr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            vorname: this.vorname,
            nachname: this.nachname
          })
        });
        const data = await res.json();
        if (res.ok) {
          this.kundenNr = data.Kunden_Nr;
        } else {
          this.fehlermeldung = data.message || 'Kunde nicht gefunden';
        }
      } catch (err) {
        this.fehlermeldung = 'Fehler bei der Verbindung zum Server';
      }
    },
    async get_StAndOrt() {
      this.anzahl = null;
      this.fehlermeldung = '';
      try {
        const res = await fetch('http://localhost:5000/api/get_StAndOrt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            stra_e: this.stra_e,
            ort: this.ort
          })
        });

        const data = await res.json();
        if (res.ok) {
          this.anzahl = data.anzahl;
        } else {
          this.fehlermeldung = data.message || 'Keine Ergebnisse gefunden';
        }
      } catch (err) {
        this.fehlermeldung = 'Fehler bei der Verbindung zum Server';
      }
    },
    async ort_max() {
        const res = await fetch('http://localhost:5000/api/ort_max')
        const data = await res.json();
        this.ort_name_max = data.ort;
        this.anzahl_ort = data.anzahl;
    }

  }
};
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