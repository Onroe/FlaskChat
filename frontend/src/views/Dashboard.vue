<template>
  <div class="container">
    <div>
  <b-navbar toggleable="lg" type="light" variant="info">
    <b-navbar-brand href="#">LiveChat</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">About</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>

        <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">SWAHILI</b-dropdown-item>
          <b-dropdown-item href="#"></b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>
            <em>Account</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item @click="logout">Log Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
   </b-navbar>
</div>
<div></div>
    <div class="row">
      <div class="col-md-3">
        <div class="card">
          <div class="card-header">Members</div>
          <div v-for="(user, id) in users" v-bind:key="id">
      <div
        v-bind:class="[activeUser == user.id ? 'user active' : 'user']"
        v-on:click="chat(user.id)"
      >
        {{user.userName}}
        <span v-if="user.has_new_message" class="has_new_message">New message</span>
        <span v-if="user.is_online" class="online"></span>
      </div>
    </div>
        </div>
      </div>

      <div class="col-md-9">
        <div class="card">
          <div class="card-header">Chats</div>

          <div class="card-body">
              <div class="messagelist" v-for="(msg, index) in messages" :key="index">
                <div class="chat-message col-md-5"
          v-bind:class="[(msg.from_user == activeUser) ? 'to-message' : 'from-message offset-md-7']">
          {{msg.message}} <span class="timestamp">{{msg.timestamp}}</span>  {{ getSentiment(msg.sentiment.polarity) }}
                </div>
                <!--  <p><span class="mt-user"> {{ user }}</span>&#32;         <span>{{ msg.message }}</span>   <span>{{ msg.timestamp }}</span></p> !-->
              </div>
            <hr />

            <form @submit.prevent="send_message" method="post">
              <div class="input-group">
                <input
                  type="text"
                  v-model="message"
                  class="form-control"
                  placeholder="Type your message..."
                />

                <div class="input-group-append">
                  <button class="btn btn-primary">Send</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import VueSocketIO from 'vue-socket.io';
// import SocketIO from 'socket.io-client';
// const socket = SocketIO('http://socketserver.com:1923');
import SocketIO from 'socket.io-client';
import axios from 'axios';
import router from '../router';


export default {
  name: 'Dashboard',
  props: {
    usern: Array,
  },
  data() {
    return {
      activeUser: null,
      token: '',
      users: [],
      userList: [],
      user: '',
      message: '',
      messages: [],
      sender_user_id: '',
      socket: SocketIO('http://localhost:5000/'),
      active_chat_id: null,
      active_chat_index: null,
      current_chat_channel: null,
      happy: String.fromCodePoint(0x1f600),
      neutral: String.fromCodePoint(0x1f610),
      sad: String.fromCodePoint(0x1f61f),
    };
  },
  created() {
    this.user = sessionStorage.getItem('username');
    this.token = sessionStorage.getItem('authToken');
    this.sender_user_id = sessionStorage.getItem('id');
    this.userlist();
  },
  methods: {
    sendMessage(e) {
      e.preventDefault();
      this.socket.emit('event', {
        user: this.user,
        message: this.message,
        timestamp: this.date(),
      });
      this.message = '';
    },

    send_message() {
      this.socket.emit('event', {
        from_user: this.sender_user_id,
        to_user: this.active_chat_id,
        message: this.message,
        channel: this.current_chat_channel,
        timestamp: this.date(),

      });
      this.message = '';
    },

    logout() {
      sessionStorage.removeItem('authToken');
      sessionStorage.removeItem('refToken');
      sessionStorage.removeItem('username');
      router.push('/login');
    },
    chat(id) {
      this.activeUser = id;
      this.request_chat(id);
    },
    // Get all users excluding the current logged user
    userlist() {
      axios.get('http://localhost:5000/api/userlist', {
        headers: { Authorization: `Bearer ${this.token}` },
      }).then((response) => {
        this.userList = response.data;
        this.users = this.userList.filter(
          (user) => user.userName !== sessionStorage.getItem('username'),
        );
      })
        .catch((error) => {
          console.log(error.response.data);
          const message = error.response.data.msg;
          if (message === 'Token has expired') {
            alert('Session expired');
            router.push('/login');
          }
        });
    },

    messagelist(id) {
      axios.post('http://localhost:5000/api/getmessages', { channelid: id }, {
        headers: { Authorization: `Bearer ${this.token}` },
      }).then((response) => {
        console.log(response.data);
        const chatmessages = response.data;
        for (let i = 0; i < chatmessages.length; i++) {
          this.messages.push(chatmessages[i]);
        }
      })
        .catch((error) => {
          console.log(error.response.data.msg);
        });
    },
    date() {
      const today = new Date();
      const date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
      const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
      const dateTime = `${date} ${time}`;
      // this.timestamp = dateTime;
      return dateTime;
    },
    // Initiate chat session
    request_chat(id) {
      this.active_chat_id = id;
      // Get index of the current chatting user...
      this.active_chat_index = this.users.findIndex(
        (user) => user.id === this.active_chat_id,
      );
      axios.post('http://localhost:5000/api/initiatechat',
        {
          from_user: this.sender_user_id,
          to_user: this.active_chat_id,
        },
        { headers: { Authorization: `Bearer ${this.token}` } })
        .then((response) => {
          this.users[this.active_chat_index].channel_name = response.data.channel_name;
          this.current_chat_channel = response.data.channel_name;

          console.log(response.data);
          this.messagelist(response.data.channel_name);
          // this.messages[response.data.channel_name].push({
          //  message: data.message,
          //  from_user: data.from_user,
          //  to_user: data.to_user,
          //   channel: data.channel_id,
          // });
        })

        .catch((error) => {
          console.log(error);
        });
    },
    getSentiment(sentiment) {
      if (sentiment > 0.5) {
        return this.happy;
      } if (sentiment < 0.0) {
        return this.sad;
      }
      return this.neutral;
    },
  },

  mounted() {
    this.socket.on('RESPONSE', (data) => {
      this.messages = [...this.messages, data];
      // you can also do this.messages.push(data)
    });
  },
};
</script>

<style scoped>
.messagelist{
 font-size: 12px;
 font-weight: bold;
 color: #999;
}
.row{
  margin-top: 10pt;
}
.user {
  margin: 0px !important;
  padding: 10px 4px 10px 8px;
  border-bottom: 1px solid gray;
}
.active {
  background: #17a2b8;
  color: white;
}
.online {
  height: 15px;
  width: 15px;
  background-color: #17a2b8;
  border-radius: 50%;
  display: inline-block;
  margin-bottom: -4px;
  border: 1px solid white;
}

.mt-user {
  padding-left: 0.25m !important;
  padding-right: 0.25m !important;
}
.from-message {
  background: #17a2b8;
  color: white;
  border-radius: 3px;
  padding: 8px 2px;
  margin-bottom: 4px;
}
.to-message {
  background: rgb(201, 209, 209);
  color: rgb(41, 53, 52);
  border-radius: 3px;
  padding: 8px 2px;
  margin-bottom: 4px;
}
.timestamp{
font-size: 8px;
}

</style>
