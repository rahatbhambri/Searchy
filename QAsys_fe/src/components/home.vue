<template>
  <router-view></router-view>
  <div id="mid-sec">
    <div id="main-text">[[ this.curr_text ]]</div>
    <div id="oth-text">
      <strong>Search for free </strong>
      <router-link to="/searchy"><button id="go">-></button></router-link>
    </div>
  </div>
</template>

<style scoped>
#mid-sec {
  margin: 0;
  height: 100vh;
  display: flex;
  flex-direction: column; /* Arrange the child elements vertically */
  position: relative;
  justify-content: center;
  align-items: center;
  background-color: aqua; /* Background color of the page */
  margin-left: 100%;
}

#main-text {
  color: black; /* Black color */
  font-family: "Pacifico", "cursive";
  font-size: 128px; /* Specific font size */
}
#oth-text {
  margin-left: 80px;
  width: 200px;
  align-items: center;
}
#go:hover {
  background-color: greenyellow;
}
</style>

<script>
export default {
  el: "#home",
  data() {
    return {
      main_text: "Searchy!",
      curr_text: "",
    };
  },
  mounted() {
    var text = this.main_text;
    let index = 0;
    const startTyping = () => {
      if (index < text.length) {
        console.log("runnig");
        this.curr_text = text.slice(0, index + 1); // Updated to include the current character
        index++;
        setTimeout(startTyping, Math.random() * 45 + 10);
      }
    };
    startTyping();
  },
  methods: {},
};
</script>
