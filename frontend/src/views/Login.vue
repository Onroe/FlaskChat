<template>
<div class="col-md-12">
  <div class="card card-container">
    <h4></h4>
     <img
        id="profile-img"
        src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
        class="profile-img-card"
      />
    <form name="form" @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <div>
        <input id="username" type="text" v-model="username"  class="form-control" required autofocus />
        </div>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
       <div>
          <input id="password" type="password" v-model="password" class="form-control" required />
        </div>
      </div>
      <div class="form-group">
     <!-- this is where we call the login function -->
      <button class="btn btn-primary btn-block" type="submit">
           <!--  <span v-show="loading" class="spinner-border spinner-border-sm"></span> -->
            <span>Login</span>
          </button>
      </div>
      <div>
        <button class="but" type="button" onclick="window.location.href = '/register';">Create account</button>
      </div>
    </form>
  </div>
  </div>
</template>
<script>
import axios from 'axios';
import router from '../router';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      proccessing: false,
      message: '',
      authenticated: false,
    };
  },
  methods: {
    login() {
      const credentials = { username: this.username, password: this.password };
      console.log(credentials);
      axios.post('http://localhost:5000/api/signin', credentials)
        .then((res) => {
          this.authenticated = true;
          sessionStorage.setItem('authToken', res.data.token);
          sessionStorage.setItem('refToken', res.data.ref_token);
          sessionStorage.setItem('username', res.data.username);
          sessionStorage.setItem('id', res.data.id);
          alert(res.data.message);
          router.push('/dashboard');
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    //  }
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
.link {
    padding-bottom: 3px;
    padding-top: 9px;
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
