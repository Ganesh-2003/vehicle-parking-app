<template>
  <div class="login">
    <h2>Login</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="loginUser">Login</button>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return { email: "", password: "" };
  },

  methods: {
    async loginUser() {
      try {
        const res = await api.post("/login", {
          email: this.email,
          password: this.password,
        });

        alert("Login successful!");
        console.log(res.data);
      } catch (err) {
        alert("Login failed");
      }
    }
  }
};
</script>