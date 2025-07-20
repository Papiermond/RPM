<template>
  <button @click="$emit('click')">
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Submit_Button'
}
</script>

<style scoped>
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #369870;
}
</style><template>
  <button @click="$emit('click')">
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Submit_Button'
}
</script>

<style scoped>
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #369870;
}
</style>