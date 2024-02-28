<template>
    <div class="sidebar">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        </ul>
    </div>
  </template>
  
  <script>
    export default {
        name: 'Sidebar',
    };
  </script>
  
  <style scoped>
  /* Customize your sidebar styles here */
  .sidebar {
    background-color: #f5f5f5;
    width: 200px;
    padding: 10px;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
  }
  </style>