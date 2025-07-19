<template>
  <div>
    <input v-model="inputValue" type="text" placeholder="Type something..." />
    <Submit_Button @click="handleClick">Submit</Submit_Button>
  </div>
</template>

<script>
import Submit_Button from "./Submit_Button.vue";

export default {
  components: { Submit_Button },
  data() {
    return {
      inputValue: ''
    }
  },
  methods: {
   async handleClick() {
      try {
        const response = await fetch('http://localhost:5000/api/get_customer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ value: this.inputValue })
        });

        const result = await response.json();
        console.log('Flask says:', result);
      } catch (error) {
        console.error('Failed to contact Flask backend:', error);
      }
    }
  }
}
</script>

<style scoped>
input {
  padding: 0.5rem;
  margin-right: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
