<template>
  <div>{{ message }}</div>
  <div>{{ message_auth }}</div>
  <div>{{ message_expo }}</div>
  <div>{{ message_download }}</div>
</template>

<script>
export default {
  data() {
    return { message: '',message_auth: '', message_expo: '',message_download: '' }
  },
  mounted() {
    fetch('http://localhost:5000/api/data')
      .then(res => res.json())
      .then(data => { this.message = data.message });
    fetch('http://localhost:5000/api/auth')
      .then(res => res.json())
      .then(data => { this.message_auth = data.message });
    fetch('http://localhost:5000/api/download')
      .then(res => res.json())
      .then(data => { this.message_download = data.message });
    fetch('http://localhost:5000/api/expo')
      .then(res => res.json())
      .then(data => { this.message_expo = data.message });
  }

}
</script>
