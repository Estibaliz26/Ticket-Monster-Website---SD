<template>
  <div class="container-login">
    <div class="myCard">
      <div class="row">
        <div class="col-md-6">
          <div class="myLeftCtn">
            <form class="myForm text-center">
              <div v-if="signincheck">
                <header>Sign In</header>
              </div>
              <div v-else>
                <header>Create Account</header>
              </div>
              <div class="form-group">
                <font-awesome-icon icon="user" size="sm" style="color: #9b00e8; position: absolute; margin: 15px"/>
                <input class="myInput" type="text" placeholder="Username" id="username" required autofocus v-model="username">
              </div>
              <div class="form-group">
                <font-awesome-icon icon="lock" size="sm" style="color: #9b00e8; position: absolute; margin: 15px"/>
                <input class="myInput" type="password" id="password" placeholder="Password" required v-model="password">
              </div>

              <div class="form-group">
                <label>
                  <input id="check_1" name="check_1"  type="checkbox" style="color: #b726ff" required>
                    <small>
                      I have read and agree to Terms & Conditions
                    </small>
                  <div class="invalid-feedback">You must check the box.</div>
                </label>
              </div>

              <div v-if="signincheck">
                <a href="#" type="submit" class="butt" @click="checkLogin" style="color: #ffffff;">LOG IN</a>
                <a href="#" type="submit" class="butt2" @click="createAccount" style="color: #b726ff;">CREATE ACCOUNT</a>
                <a href="#" type="submit" class="butt3" @click="goToShows" style="color: #b726ff;">BACK TO SHOWS</a>
              </div>
              <div v-else>
                <a href="#" type="submit" class="butt" @click="onSubmit" style="color: #ffffff;">SUBMIT</a>
                <a href="#" type="submit" class="butt3" @click="returnToLogin" style="color: #b726ff;">RESET</a>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import '../../bootstrap/css/bootstrap.css'
import axios from 'axios'

export default {
  data () {
    return {
      username: '',
      password: '',
      name: 'Login',
      addUserForm: {
        username: '',
        password: ''
      },
      signincheck: true,
      isadmin: false
    }
  },
  methods: {
    initForm () {
      this.addUserForm.username = ''
      this.addUserForm.password = ''
    },
    createAccount () {
      this.signincheck = false
    },
    returnToLogin () {
      this.signincheck = true
    },
    getAccount () {
      const path = `http://localhost:5000/account/` + this.username
      axios.get(path)
        .then((res) => {
          this.isadmin = res.data.account.admin
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          // TODO catch timeout
        })
    },
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      const path = `http://localhost:5000/login`
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.getAccount()
          this.$router.replace({ path: '/', query: { username: this.username, logged: this.logged, token: this.token } })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username or Password incorrect')
          // TODO catch timeout
        })
    },
    goToShows () {
      this.$router.replace({path: '/', query: {}})
    },
    onSubmit () {
      const parameters = {
        username: this.username,
        password: this.password,
        money: 1000 // regalito
      }
      const path = `http://localhost:5000/account`
      axios.post(path, parameters)
        .then((res) => {
          // TODO
          alert('An account has been created')
        })
        .catch((error) => {
          // TODO
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username or Password incorrect')
        })
    }
  }
}
</script>

<style scoped>

</style>
