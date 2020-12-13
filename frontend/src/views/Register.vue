<template>
<div class="col-md-12">
  <div class="card card-container">
    <h4></h4>
     <img
        id="profile-img"
        src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
        class="profile-img-card"
      />
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <div>
        <input id="username" type="type" v-model="username"  rules="rules.username" class="form-control" required autofocus />
        </div>
      </div>
      <div class="form-group">
        <label for="username">Email Address</label>
        <div>
        <input id="email" type="email" v-model="email" class="form-control" required autofocus />
        </div>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
       <div>
          <input  name="password" id="password" type="password"  class="form-control" v-model="password" required />
        </div>
      </div>
      <div class="form-group">
        <label for="password">Confirm Password</label>
       <div>
          <input name="cpassword" id="cpassword" type="password" v-model="cpassword"  class="form-control" required />
        </div>
      </div>
      <div class="form-group">
     <!-- this is where we call the login function -->
      <button class="btn btn-primary btn-block" :disabled="loading">
            <span v-show="loading" class="spinner-border spinner-border-sm"></span>
            <span>Register</span>
          </button>
      </div>
      <div>
        <button class="but" type="button" onclick="window.location.href = '/login';">Login</button>
      </div>
    </form>
  </div>
  </div>
</template>
<script>
import { required, sameAs, minLength } from 'vuelidate/lib/validators';
import axios from 'axios';
import router from '../router';

export default {
  name: 'Register',
  data() {
    return {
      loading: false,
      email: '',
      username: '',
      password: '',
      cpassword: '',
      rules: {
        username: [
          (v) => !!v || 'Username is required',
          (v) => (v && v.length > 3) || 'A username must be more than 3 characters long',
          (v) => /^[a-z0-9_]+$/.test(v) || 'A username can only contain letters and digits',
        ],
        password: [
          (v) => !!v || 'Password is required',
          (v) => (v && v.length > 7) || 'The password must be longer than 7 characters',
        ],
      },
      validations: {
        password: {
          required,
          minLength: minLength(6),
        },
        cpassword: {
          sameAsPassword: sameAs('password'),
        },
      },

    };
  },
  computed: {
    loggedIn() {
      return this.username;
    },
  },
  mounted() {
    if (this.loggedIn) {
      this.$router.push('/dashboard');
    }
  },
  methods: {
    register() {
      const details = { username: this.username, password: this.password, cpassword: this.cpassword };
      axios.post('http://localhost:5000/api/signup', details).then((response) => {
        alert(response.data.message);
        // if (response.data.status === 'success') {
        router.push('/login');
        // }
      })
        .catch((response) => {
          alert(response.data.message);
        });
    },
  },
};
</script>
<style scoped>
label {
  display: block;
  margin-top: 10px;
}

.card-container.card {
  max-width: 350px !important;
  padding: 40px 40px;
}

.card {
  background-color: #f7f7f7;
  padding: 20px 25px 30px;
  margin: 0 auto 25px;
  margin-top: 50px;
  -moz-border-radius: 2px;
  -webkit-border-radius: 2px;
  border-radius: 2px;
  -moz-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
}

.profile-img-card {
  width: 96px;
  height: 96px;
  margin: 0 auto 10px;
  display: block;
  -moz-border-radius: 50%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
}
.but {
  border-radius: 4px;
color: #1a73e8;
display: inline-block;
font-weight: 500;
letter-spacing: .25px;
background-color: transparent;
border: 0;
cursor: pointer;
font-size: inherit;
outline: 0;
padding: 0;
text-align: left;
}
</style>
