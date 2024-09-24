<template>
  <router-view></router-view>

  <div
    id="app_main"
    class="row align-items-start justify-content-right container mt-3 bg-gradient-light border border-primary rounded"
    style="font-family: 'Pacifico', cursive"
  >
    <div class="col sidebar bg-gradient-light border border-primary rounded">
      <ul class="sidebar-ul">
        <li><router-link style="color: black" to="/">+ New Chat </router-link></li>
        <li v-for="sess in sessions" :key=sess.id @click="changeSession(sess.id)">
          <router-link style="color: black" to="/hello"
            >Session [[ sess.id ]]</router-link
          >
        </li>
      </ul>
    </div>

    <div
      id="right-options"
      class="col"
      style="height: 1px; margin-left: 1120px; margin-top: 5px"
    >
      <button class="btn btn-primary" style="background-color: red">Logout</button>
    </div>

    <div
      id="main"
      class="col column justify-content-center container mt-3 bg-gradient-light border border-primary rounded"
    >
      <h1 class="font-weight-bold text-center container" id="phead">
        Searchy
        <img class="img-fluid mx-auto" id="searchy" src="/src/assets/fish.gif" />
      </h1>

      <div
        id="all_chats"
        class="container-fluid mt-3 bg-gradient-light border border-primary"
      >
        <div
          class="container mt-3 bg-gradient-light border border-primary alert alert-primary"
        >
          <ul>
            <li
              v-for="chat in chats"
              :key="chat.question"
              class="d-flex"
              style="border: 0.1in solid darkblue; background-color : #ADD8E6;"
            >
              <img :src="chat.img" id="curr_img" class="img-fluid" />
              <p class="alert alert-primary">
                <strong> Q: </strong> [[ chat.question ]]
                <br />
                <strong>Answer : </strong> [[ chat.answer ]]
              </p>
              <br />
            </li>
            <br />
          </ul>
        </div>

        <div v-if="answer_received" class="d-flex">
          <img :src="img" id="curr_img" class="img-fluid" />
          <p class="alert alert-primary">
            <strong>Q: </strong> [[ this.question ]]
            <br />
            <strong>Answer : </strong> [[ this.answer ]]
            <span class="blinking-cursor">|</span> .
          </p>
        </div>
      </div>

      <div id="asker" class="column justify-content-center">
        <form @submit.prevent style="margin-top: 15px">
          <input
            id="question"
            style="width: 600px"
            v-model="curr_question"
            placeholder="Ask me anything"
          />
          <button type="submit" @click="getAnswer()" class="btn btn-primary">
            Ask a question
          </button>
        </form>
        <br />
      </div>
    </div>
  </div>
</template>

<style scoped>
#searchy {
  width: 1in;
  height: 1in;
  display: inline;
  vertical-align: middle;
}
.sidebar {
  background-color: orange;
  width: 200px;
  padding: 10px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  color: black;
}
.sidebar-ul li:hover {
  background-color: #add8e6;
  text-decoration: underline;
  cursor: pointer;
  color: black;
}
#app_main {
  margin: 0 auto;
  margin-left: 100px;
  width: 2000px;
  height: 700px;
  background-color: aqua;
  flex-flow: row wrap;
  /* Enable vertical scrollbar */
  display: inline-block;
}
#all_chats {
  overflow: auto;
  width: 1070px;
  height: 500px;
  background-color: blue;
}
#phead {
  background-color: blue;
  color: white;
  border: 0.05in solid #add8e6;
}
#curr_img {
  width: 300px;
  height: 300px;
  border: 0.05in solid black;
}
hr {
  border: 2px solid darkblue;
}
.blinking-cursor {
  margin-left: 5px;
  background-color: #fff;
  animation: blink 1s infinite;
}
@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  50.1%,
  100% {
    opacity: 0;
  }
}
#answer {
  overflow-y: auto;
}

#asker {
  position: relative;
  margin-bottom: 10px;
  margin-left: 100px;
}
</style>

<script>
import axios from "axios";

export default {
  el: "#search",
  data() {
    return {
      question: null,
      curr_question: null,
      answer_received: false,
      answer: null,
      img: null,
      chats: [],
      sessions: [],
      curr_session_id: 1,
    };
  },
  mounted() {
    // Retrieve data from session storage
    let savedChats = sessionStorage.getItem(this.curr_session_id);
    // Check if key exists in session storage
    if (savedChats === null) {
      this.chats = [];
    } else {
      this.chats = JSON.parse(savedChats);
    }

    axios
      .get("http://127.0.0.1:5000/get_user", { params: { user_id: "jimmy@gmail.com" } })
      .then((response) => {
        this.sessions = response.data;
        console.log("session data= ", this.sessions);
      })
      .catch((error) => {
        this.sessions = [{ id: 1 }, { id: 2 }, { id: 3 }];
        console.error("Error fetching data:", error);
      });
  },
  methods: {
    async getAnswer() {
      //console.log('Server response:'.data);
      this.answer_received = false;
      this.question = this.curr_question;
      const data = { question: this.question };
      const response = await axios.get("http://127.0.0.1:5000/answer", {
        params: data,
      });
      this.answer_received = true;
      const text = response.data["answer"];
      this.img = response.data["img"];
      // console.log('Server response:', response.data);
      // console.log('Question submitted:', this.question);
      let index = 0;
      const startTyping = async () => {
        if (index < text.length) {
          this.answer = text.slice(0, index + 1); // Updated to include the current character
          index++;
          setTimeout(startTyping, Math.random() * 25 + 10);
        } else {
          this.answer = text;
          await new Promise((resolve) => setTimeout(resolve, 3000)); // Wait for 3 seconds
          this.answer_received = false;
          this.chats.push(last_chat);
        }
      };

      var last_chat = {
        question: this.question,
        answer: text,
        img: this.img,
        timestamp: new Date().toLocaleString(),
      };

      startTyping();
      sessionStorage.setItem(this.curr_session_id, JSON.stringify(this.chats));
    },
    async changeSession(session_id) {
      var data = {
        user_id: "jimmy@gmail.com",
        session_id: session_id,
      };
      const response = await axios.get("http://127.0.0.1:5000/get_chats", {
        params: data,
      });

      console.log(session_id, response.data);
      if (response !== null) {
        console.log(response);
        this.chats = response.data;
      } else {
        this.chats = [];
      }
    },
    scrollToBottom() {
      const scrollableDiv = this.$refs.scrollableDiv;
      scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
    },
  },
};
</script>
