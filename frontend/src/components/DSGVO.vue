<template>
    <button @click="$router.push('/')" class="back-button">Zurück</button>
  <div>
    <h2>DSGVO-Anfragen</h2>

    <!-- Information -->
    <form @submit.prevent="holeKundendaten">
      <input v-model="dsGvoName" placeholder="Vorname Nachname" class="input" />
      <button type="submit" class="btn">Auskunft anfordern</button>
    </form>
    <div v-if="kundenAuskunft">
      <h4>Gespeicherte Kundendaten:</h4>
        <ul>
            <li><strong>Vorname:</strong> {{ kundenAuskunft.Vorname }}</li>
            <li><strong>Nachname:</strong> {{ kundenAuskunft.Nachname }}</li>
            <li><strong>Adresse:</strong> {{ kundenAuskunft.Stra_e }}, {{ kundenAuskunft.Haus_Nr }}, {{ kundenAuskunft.PLZ }}, {{ kundenAuskunft.Ort }}</li>
        </ul>
    </div>

    <!-- Delet/ANOYM -->
    <form @submit.prevent="loescheKundendaten">
      <input v-model="dsGvoName" placeholder="Vorname Nachname" class="input" />
      <button type="submit" class="btn cancel">Daten löschen/ Anonymisiert </button>
      <div v-if="feedback" class="feedback">
         {{ feedback }}
        </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "DSGVO",
  data() {
    return {
        dsGvoName: '',
        kundenAuskunft: null,
        feedback: ''
    };
  },
  methods: {
    async holeKundendaten() {
      const [vorname, nachname] = this.dsGvoName.split(' ');
      if (!vorname || !nachname) {
        alert("Bitte Vor- und Nachname eingeben.");
        return;
      }

      const res = await fetch('http://localhost:5000/api/dsgvo_information', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vorname, nachname })
      });

      const data = await res.json();
      if (res.ok) {
        this.kundenAuskunft = data;
      } else {
        alert(data.message || "Fehler bei der Anfrage.");
      }
    },

    async loescheKundendaten() {
        const [vorname, nachname] = this.dsGvoName.split(' ');
      if (!vorname || !nachname) {
        alert("Bitte Vor- und Nachname eingeben.");
        return;
      }

      try {
        const res = await fetch('http://localhost:5000/api/dsgvo_delet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vorname, nachname })
        });

        const data = await res.json();
        if (res.ok) {
        this.feedback = data.message;
        } else {
        this.feedback = data.message || 'Fehler beim Löschen';
        }
    } catch (error) {
        this.feedback = 'Serverfehler oder keine Verbindung';
    }
    }
  }
};
</script>