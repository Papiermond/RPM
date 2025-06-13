<template>
  <div>{{ message }}</div>
</template>

<script>
export default {
  data() {
    return { message: '' }
  },
  mounted() {
    fetch('http://localhost:5000/api/data')
      .then(res => res.json())
      .then(data => { this.message = data.message });
  }
}
</script>