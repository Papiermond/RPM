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

    <form @submit.prevent="getunbestellt">
      <button type="submit" class="btn">Was nicht Bestellt wurde</button>
    </form>
    <div v-if="unbestellt.length > 0 && zeigeUnbestellt">
      <ul>
        <li v-for="p in unbestellt" :key="p.produktname">{{ p.produktname }} </li>
      </ul>
    </div>

    <form @submit.prevent="gettogether">
      <input v-model="produktnameA" placeholder="Produkt A" class="input" />
      <input v-model="produktnameB" placeholder="Produkt B" class="input" />
      <button type="submit" class="btn">Submit</button>
    </form>
    <div v-if="anzahlgemeinsam !== null">
      <strong>Gemeinsam bestellt:</strong> {{ anzahlgemeinsam }}
    </div>

    <div>
      <button @click="showModal = true" class="btn">Neue Bestellung hinzufügen</button>

      <div v-if="showModal" class="modal-backdrop">
        <div class="modal">
          <h3>Neue Bestellung</h3>

          <form @submit.prevent="submitBestellung">

            <label>Kunde:</label>
            <input list="kundenListe" v-model="form.kundenName" placeholder="Kunde" required />
            <datalist id="kundenListe">
              <option v-for="kunde in kunden" :key="kunde.Kunden_Nr" :value="`${kunde.Vorname} ${kunde.Nachname}`" />
            </datalist>

            <label>Datum:</label>
            <input v-model="form.datum" type="date" required />

            <label>Gesamtpreis:</label>
            <input v-model="form.gesamtpreis" type="Float" min="0" placeholder="Gesamtpreis" required/>

            <label>Produkt:</label>
            <input list="produktliste" v-model="neuesProduktname" placeholder="Produkt wählen" />

            <datalist id="produktliste">
              <option v-for="produkt in produkte" :key="produkt.Produkt_Nr" :value="produkt.Produktname" />
            </datalist>

            <input type="number" v-model.number="neueMenge" min="1" placeholder="Menge" />

            <select v-model="neueGroesse">
              <option disabled value="">Größe wählen</option>
              <option v-for="größe in groessenListe" :key="größe" :value="größe">
                {{ größe }}
              </option>
            </select>

            <button type="button" @click="hinzufuegenProdukt">+</button>

            <ul>
              <li v-for="(eintrag, index) in produktAuswahl" :key="index">
                {{ getProduktName(eintrag.id) }} – {{ eintrag.menge }}x - {{ eintrag.groesse }}
                <button type="button" @click="produktAuswahl.splice(index, 1)">Entfernen</button>
              </li>
            </ul>

            <button type="submit" class="btn">Hinzufügen</button>
            <button @click="showModal = false" type="button" class="btn cancel">Abbrechen</button>
          </form>
        </div>
      </div>
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
      anzahlgemeinsam: null,
      zeigeUnbestellt: false,

      showModal: false,
      kunden: [],
      produkte: [],
      form: {
      kundenNr: '',
      datum: '',
      gesamtpreis: '',
      },
      produktMengen: {},
      neueMenge: 1,
      neuesProduktId: '',
      produktAuswahl: [],
      neueGroesse: '',
      groessenListe: ['1 kg','10 kg','3 kg','100 g','500 g','250 g','Schale','Stück']
    };
  },
  mounted() {
    fetch('http://localhost:5000/api/auftraege')
      .then(res => res.json())
      .then(data => this.auftraege = data);
    
    fetch('http://localhost:5000/api/kunde')
      .then(res => res.json())
      .then(data => this.kunden = data);

    fetch('http://localhost:5000/api/produkte')
      .then(res => res.json())
      .then(data => this.produkte = data);
  },
  methods: {
    toggleDetails(nr) {
      if (this.expanded.includes(nr)) {
        this.expanded = this.expanded.filter(n => n !== nr);
      } else {
        this.expanded.push(nr);
      }
    },

    getProduktName(id) {
    const produkt = this.produkte.find(p => p.Produkt_Nr === id);
    return produkt ? produkt.Produktname : 'Unbekanntes Produkt';
    },

    getProduktIdByName(name) {
      const produkt = this.produkte.find(p => p.Produktname === name);
      return produkt ? produkt.Produkt_Nr : null;
    },

    hinzufuegenProdukt() {
      const produktId = this.getProduktIdByName(this.neuesProduktname);
      if (!produktId || this.neueMenge < 1 || !this.neueGroesse) return;

      const existiert = this.produktAuswahl.find(e => e.id === produktId && e.groesse === this.neueGroesse);
      if (existiert) {
        existiert.menge += this.neueMenge;
      } else {
        this.produktAuswahl.push({
          id: produktId,
          menge: this.neueMenge,
          groesse: this.neueGroesse
        });
      }

      this.neuesProduktname = '';
      this.neueMenge = 1;
      this.neueGroesse = '';
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
      
    },

    async getunbestellt() {
      this.zeigeUnbestellt = !this.zeigeUnbestellt;

      const res = await fetch('http://localhost:5000/api/unbestellte_produkte',);

      const data = await res.json();
      this.unbestellt = data
      
    },

    async gettogether() {
      this.anzahlgemeinsam = null;
      try {
          const res = await fetch('http://localhost:5000/api/produkte_together',{
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                  produktnameA: this.produktnameA,
                  produktnameB: this.produktnameB
              })          
              });
              const data = await res.json();
              if (res.ok) {
                  this.anzahlgemeinsam = data.anzahl;
              }
              else {
                    this.anzahlgemeinsam = 'Nicht gefunden';
              }
          } 
          catch (err) {
              this.anzahlgemeinsam = 'Fehler beim Laden';
          }
    },

    async submitBestellung() {
      const kunde = this.kunden.find(
      k => `${k.Vorname} ${k.Nachname}` === this.form.kundenName
      );

      const kundenNr = kunde ? kunde.Kunden_Nr : null;

      if (!kundenNr) {
        alert("Kunde nicht gefunden!");
        return;
      }

      const produkteMitMenge = this.produktAuswahl.map(p => ({
        produktNr: p.id,
        menge: p.menge,
        groesse: p.groesse
      }));

      const payload = {
        kundenNr: kundenNr,
        datum: this.form.datum,
        gesamtpreis: this.form.gesamtpreis,
        produkte: produkteMitMenge
      };

      console.log('Sende Bestellung:', payload);

      const res = await fetch('http://localhost:5000/api/auftrag_hinzufuegen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      if (res.ok) {
        alert("Bestellung erfolgreich gespeichert");
        this.showModal = false;

        this.form = { kundenNr: '', datum: '', gesamtpreis: '' };
        this.produktMengen = {};
      } else {
        alert(data.message || "Fehler beim Hinzufügen");
      }
    }
  }
}

</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  min-width: 1000px;
  max-height: 200vh;
  overflow-y: auto;
}

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
