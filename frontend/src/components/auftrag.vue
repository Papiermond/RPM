<template>
  <div>
    <button @click="$router.push('/')" class="back-button">Zurück</button>
    <h2>Aufträge</h2>
    <form @submit.prevent="auftrag_anzahl">
        <input v-model="vorname" placeholder="Vorname" class="input" />
        <input v-model="nachname" placeholder="Nachname" class="input" />
        <button type="submit" class="btn"> Submit </button>
    </form>
    <div v-if="anzahl_Auftrag !== null">
        <strong>Anzahl Aufträge:</strong> {{ anzahl_Auftrag }}
        <strong>Anzahl Aufträge:</strong> {{ parseFloat(gesamtumsatz).toFixed(2) }} €
    </div>

    <form @submit.prevent="getKundeByAuftrag">
        <input v-model="Auftrag_Nr" placeholder="Auftrag Nr." class="input" />
        <button type="submit" class="btn"> Submit </button>
    </form>
    <div v-if="Kunde">
        <strong>Kunde:</strong> {{ Kunde.vorname }} {{ Kunde.nachname }}
    </div>
    <div v-if="fehlermeldung" style="color: red;">
        {{ fehlermeldung }}
    </div>

    <form @submit.prevent="getProduktOrder">
      <input v-model="produktname" placeholder="Produktname" class="input" />
      <button type="submit" class="btn">Submit</button>
    </form>
    <div v-if="anzahlProdukt1 !== null">
      <strong>Bestellungen:</strong> {{ anzahlProdukt1 }}
    </div>

    <form @submit.prevent="getProduktMonat">
      <input v-model="monat" type="month" class="input" />
      <button type="submit" class="btn">Submit</button>
    </form>
    <div v-if="produkteMonat.length > 0">
      <ul>
        <li v-for="p in produkteMonat" :key="p.Produktname">{{ p.Produktname }} – {{ p.anzahl }}x</li>
      </ul>
    </div>

    <table class="auftragstabelle">
      <thead>
        <tr>
          <th class="border p-2">Auftrag Nr</th>
          <th class="border p-2">Vorname</th>
          <th class="border p-2">Nachname</th>
          <th class="border p-2">Datum</th>
          <th class="border p-2">Gesamtpreis</th>
          <th class="border p-2">Produkte anzeigen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="auftrag in auftraege" :key="auftrag.auftrag_Nr">
          <td class="border p-2">{{ auftrag.Auftrag_Nr }}</td>
          <td class="border p-2">{{ auftrag.vorname }}</td>
          <td class="border p-2">{{ auftrag.nachname }}</td>   
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
                    <th class="border p-2">Produkt Anzahl</th>
                    <th class="border p-2">Produktgröße</th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="produkt in auftrag.produkte" :key="produkt.produkt_Nr">
                    <td class="border p-2">{{ produkt.Produkt_Nr }}</td>
                    <td class="border p-2">{{ produkt.Produktname }}</td>
                    <td class="border p-2">{{ produkt.Produkt_Anzahl }}</td>
                    <td class="border p-2">{{ produkt.Produktgröße }}</td>
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
      expanded: [],
      vorname: '',
      nachname: '',
      anzahl_Auftrag: null,
      gesamtumsatz: null,
      Kunde: null,
      fehlermeldung: '',
      produktname: '',
      anzahlProdukt1: null,
      monat: '',
      produkteMonat: [],
      unbestellt: [],
      produktnameA: '',
      produktnameB: '',
      anzahlgemeinsam: null
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
    },

    async auftrag_anzahl() {
        this.anzahl_Auftrag = null;
        this.gesamtumsatz = null;
        try {
            const res = await fetch('http://localhost:5000/api/anzahl_auftrag',{
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    vorname: this.vorname,
                    nachname: this.nachname
                })          
                });
                const data = await res.json();
                if (res.ok) {
                    this.anzahl_Auftrag = data.anzahl;
                    this.gesamtumsatz = data.umsatz;
                }
                else {
                     this.anzahl_Auftrag = 'Nicht gefunden';
                }
            } 
            catch (err) {
                this.anzahl_Auftrag = 'Fehler beim Laden';
            }
        },
    
    async getKundeByAuftrag() {
        this.Kunde = null;
        this.fehlermeldung = '';

        try {
            const res = await fetch('http://localhost:5000/api/get_kunde_by_auftrag', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ Auftrag_Nr: this.Auftrag_Nr })
            });

            const data = await res.json();
            if (res.ok) {
            this.Kunde = data;
            } else {
            this.fehlermeldung = data.message || 'Kein Kunde gefunden.';
            }
        } catch (err) {
            this.fehlermeldung = 'Serverfehler oder keine Verbindung.';
        }
    },

    async getProduktOrder() {
        this.anzahlProdukt1 = null;

        const res = await fetch('http://localhost:5000/api/produkt_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ produktname: this.produktname })
        });

        const data = await res.json();
        this.anzahlProdukt1 = data.anzahl
    },

    async getProduktMonat() {
      this.produkteMonat = [];

      const res = await fetch('http://localhost:5000/api/produkte_monat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ monat: this.monat })
      });

      const data = await res.json();
      this.produkteMonat = data
      
    }
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
