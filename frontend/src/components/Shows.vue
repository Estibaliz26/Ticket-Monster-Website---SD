<template style=" background-color: #421e53">
  <div id="app" style="margin-top: 0; padding-top: 0; padding-bottom: 8rem;">
    <header class="header">
      <div class="bg-transparent" style="padding-top: 1rem;">
        <div class="container">
          <nav class="navbar navbar-expand-lg navbar-light">
            <a class="navbar-brand justify-content-start" style="color: white; font-family: 'Roboto', sans-serif">
              Money available {{this.money_available}}€
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
              <div class="navbar-nav w-100 justify-content-end">
                <div v-if="logged && !is_admin">
                  <button class="btn btn-outline-success" type="submit" @click="isShowingCart = true" style="margin-right: 1.5rem; margin-left: 1.5rem; position: relative">
                    <font-awesome-icon icon="shopping-basket" size="lg" style="color: #ffffff"/>
                    <div class="num_items_cart" v-if="count_items_added > 0">
                      <span> {{ this.count_items_added }} </span>
                    </div>
                  </button>
                </div>
                <div v-if="logged">
                  <a class="nav-item a-neon" href="#" @click="forgetUser" style="font-size: 17px;">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    Log Out
                  </a>
                </div>
                <div v-else>
                  <a class="nav-item a-neon" href="#" @click="goToLogin">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    Log In
                  </a>
                </div>
              </div>
            </div>
          </nav>
        </div>
      </div>
      <br>
    </header>

    <div v-if="isShowingCart === false">
      <div v-if="is_admin">
        <a href="#" class="btn btn-primary" @click="showFormNew" style="margin-right: 3rem">Add Event</a>
        <a href="#" class="btn btn-primary" @click="showFormModify">Modify Event</a>
      </div>
      <div class="row row-cols-1 row-cols-md-3" style="margin-left: 8rem; margin-right: 8rem" id="content">
        <div class="col-lg-4 col-sm-6 mb-4" style="position: center" v-for="(show) in shows" :key="show.id">
          <br>
          <div class="card-shows">
            <img class="card-img-top" src="../assets/lilac.png" alt="Card image cap">
            <div class="white-box" style="width: 4rem; height: 4rem; margin: 0.5rem">
              <h6 style="font-family: 'Roboto'; font-weight: normal">{{ show.month }}</h6>
              <h6 style="font-family: 'Roboto'; font-weight: bold; font-size: 1.3rem">{{ show.day }}</h6>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ show.name }}</h5>
              <hr>
              <p class="card-text">
              <div v-for="(artist) in show.artists" :key="artist.id">
                <h6 class="card-text">{{ artist.name }}</h6>
              </div>
              <br>
              <font-awesome-icon icon="map-marker-alt" size="lg" style="color: #ffffff"/> {{ show.place.name }}, {{ show.place.city }}
              <h6 class="price">
                <h4>{{ show.price }}<sup>€</sup></h4>
              </h6>
              <p class="card-text"><small class="text-muted" style="color: #ffffff">{{ show.total_available_tickets }} tickets available</small></p>
              <div v-if="logged">
                <div v-if="is_admin">
                  <a href="#" class="btn btn-primary" @click="showFormAddArtist (show)">Add Artist</a>
                  <p></p>
                  <a href="#" class="btn btn-primary" @click="showFormRemoveArtist (show)">Remove Artist</a>
                  <p></p>
                  <a href="#" class="btn btn-primary" @click="removeShow (show)">Delete Event</a>
                </div>
                <div v-else>
                  <a href="#" class="btn btn-primary" @click="addShowToCart (show)">Add to cart</a>
                </div>
              </div>
              <div v-else>
                <a href="#" class="btn btn-primary" @click="goToLogin ()">Log in to buy</a>
              </div>

            </div>
          </div>
        </div>
      </div>

      <b-modal ref="addShowModal"
               id="event-modal"
               title="Add new event"
               hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" v-if="show_modal_toggle">
          <b-form-group label="Name:" label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="addShowForm.name"
              placeholder="Enter event name"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Price:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="addShowForm.price"
              type="number"
              placeholder="Enter price"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Date:" label-for="input-3">
            <b-form-datepicker date-disabled-fn="dateDisabled"
                               id="input-3"
                               v-model="addShowForm.date"
                               required
            ></b-form-datepicker>
          </b-form-group>

          <b-form-group label="Place:" label-for="input-6">
            <b-form-input
              id="input-6"
              v-model="addShowForm.place"
              placeholder="Enter name place"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="city:" label-for="input-8">
            <b-form-input
              id="input-8"
              v-model="addShowForm.city"
              placeholder="Enter city"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="country:" label-for="input-9">
            <b-form-input
              id="input-9"
              v-model="addShowForm.country"
              placeholder="Enter country"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Tickets:" label-for="input-7">
            <b-form-input
              id="input-7"
              v-model="addShowForm.total_available_tickets"
              type="number"
              placeholder="Enter tickets"
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>

      <b-modal ref="editShowModal"
               id="event-modal"
               title="Update event"
               size="lg"
               hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onReset" v-if="show_modal_toggle">
          <b-form-group label="Id:" label-for="input-0">
            <b-form-input
              id="input-0"
              v-model="editShowForm.id"
              type="number"
              placeholder="Enter id"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Name:" label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="editShowForm.name"
              placeholder="Enter event name"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Price:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="editShowForm.price"
              type="number"
              placeholder="Enter price"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Date:" label-for="input-3">
            <b-form-datepicker
              id="input-3"
              v-model="editShowForm.date"
            ></b-form-datepicker>
          </b-form-group>

          <b-form-group label="Place:" label-for="input-6">
            <b-form-input
              id="input-6"
              v-model="editShowForm.place"
              placeholder="Enter name place"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="city:" label-for="input-8">
            <b-form-input
              id="input-8"
              v-model="editShowForm.city"
              placeholder="Enter city"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="country:" label-for="input-9">
            <b-form-input
              id="input-9"
              v-model="editShowForm.country"
              placeholder="Enter country"
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Tickets:" label-for="input-7">
            <b-form-input
              id="input-7"
              v-model="editShowForm.total_available_tickets"
              type="number"
              placeholder="Enter tickets"
              required
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>

      <b-modal ref="addArtistModal"
               id="artist-modal"
               title="Add artist"
               hide-footer>
        <b-form @submit="onSubmitAddArtistInShow" @reset="onResetAddArtistInShow" v-if="show_modal_toggle">
          <b-form-group label="Name:" label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="addArtistForm.name"
              placeholder="Enter artist name"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group label="Country:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="addArtistForm.country"
              placeholder="Enter country"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-3" label="Genre:" label-for="input-3">
            <b-form-checkbox-group
              id="input-3"
              v-model="addArtistForm.genres"
            >
              <b-form-checkbox style="caret-color: #0c5460" value="MUSIC">Music</b-form-checkbox>
              <b-form-checkbox value="THEATRE">Theatre</b-form-checkbox>
              <b-form-checkbox value="DANCE">Dance</b-form-checkbox>
              <b-form-checkbox value="CIRCUS">Circus</b-form-checkbox>
              <b-form-checkbox value="OTHER">Other</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>

      <b-modal ref="removeArtistModal"
               id="remove-artist-modal"
               title="Remove artist"
               hide-footer>
        <b-form @submit="onSubmitRemoveArtistInShow" @reset="onResetRemoveArtistInShow">
          <b-form-group label="Select artist name:" label-for="select-name">
            <b-form-select
              id="select-name"
              v-if="show_to_modify"
              v-model="removeArtistForm.name">
              <b-form-select-option id="artistname" v-for="artist in show_to_modify.artists" v-bind:value="artist" :key="artist.id" required>
                {{ artist.name }}</b-form-select-option>
            </b-form-select>
          </b-form-group>

          <b-form-group label="Id:" label-for="input-id">
            <b-form-input
              id="input-id"
              v-model="removeArtistForm.id"
              placeholder="Artist id"
              type="text"
              disabled
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>
    </div>

    <div class="container" id="cart-container" v-else align="center">
      <div class="card" style="background-color: rgba(255, 255, 255, 0.2); color: white; height: 15rem; width: 30rem" v-if="shows_added.length === 0">
        <h2 style="text-align: center; padding: 8vh">Your cart is empty</h2>
        <div class="cart-buttons">
          <button class="btn cart-btn" @click="isShowingCart = false">Back</button>
        </div>
      </div>
      <div class="card" v-if="shows_added.length > 0">
        <div class="row">
          <div class="col-md-8 cart">
            <div class="title-basket">
              <div class="row" style="margin: 0">
                <div class="col">
                  <h4><b>Shopping Cart</b></h4>
                </div>
                <div class="col align-self-center text-right text-muted">{{this.count_items_added}} items</div>
              </div>
            </div>
            <table v-if="shows_added.length > 0" class="styled-table">
              <thead>
              <tr>
                <th> </th>
                <th>Event</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
                <th></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(show) in shows_added" :key="show.id">
                <td align="center"><img class="img-fluid" src="../assets/lilac.png" style="width: 5rem; border-radius: 0.3rem"></td>
                <td align="center">{{ show.name }}</td>
                <td align="center">
                  <button v-on:click="decrementTicket(show)" class="btn rm-btn" style="line-height: 1rem">-</button>
                  {{ show.quantity }}
                  <button v-on:click="addShowToCart(show)" class="btn add-btn" style="line-height: 1rem">+</button>
                </td>
                <td align="center">{{ show.price }} €</td>
                <td align="center">{{ show.quantity * show.price }} €</td>

                <td align="center">
                  <button v-on:click="deleteShowTickets(show)" class="btn cart-btn del-btn" style="background: transparent">
                  <font-awesome-icon icon="trash-alt" size="lg" style="color: #000000"/> Remove item
                  </button>
                </td>
              </tr>
              </tbody>
            </table>
            <div class="cart-buttons">
              <button class="btn cart-btn" @click="isShowingCart = false">Back</button>
            </div>
          </div>

          <div class="col-md-4 summary-basket" v-if="shows_added.length > 0">
            <div>
              <h5 style="margin-top: 4vh; color: white"><b>Summary</b></h5>
            </div>
            <hr>
            <div class="row" style="margin: 0">
              <div class="col" style="padding-left:0; font-family: sans-serif; font-size: 0.9rem; font-weight: bold; vertical-align: middle; color: white">
                ITEMS {{ this.count_items_added }}
              </div>
              <div class="col text-right" style="color: white">&euro; 132.00</div>
            </div>
            <form style="padding: 3vh 0; margin: 0">
              <p style="margin-left:0; font-family: sans-serif; font-weight: bold; font-size: 0.9rem; color: white">DISCOUNT CODE</p>
              <input id="code" style="border: 1px solid rgba(0, 0, 0, 0.137); padding: 1vh;margin-bottom: 4vh;outline: none;background-color: rgba(255, 255, 255, 0.2)" placeholder="Enter your code">
            </form>
            <div class="row" style="border-top: 1px solid rgba(0,0,0,.1); padding: 2vh 0; margin: 0">
              <div class="col" style="font-family: sans-serif; vertical-align: middle; font-weight: bold; font-size: 0.9rem; color: white">
                TOTAL AMOUNT
              </div>
              <div class="col text-right" style="color: white">&euro; 137.00</div>
            </div> <button class="btn-checkout" v-on:click="finalizePurchase" v-if="shows_added.length > 0">CHECKOUT</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import '../../bootstrap/css/bootstrap.css'

export default {
  data () {
    return {
      tickets_bought: 0,
      tickets_available: 500,
      money_available: 300,
      money_total: 72,
      price_event: 30,
      total_tickets: 20,
      remaining_tickets: 20,
      logged: false,
      cart_empty: true,
      is_admin: false,
      username: '',
      token: '',
      show_modal_toggle: false,
      shows_added: [],
      all_shows_id_added: new Set(),
      count_items_added: 0,
      isShowingCart: false,
      tickets: [],
      addShowForm: {
        place: '',
        name: '',
        city: '',
        date: '',
        price: '',
        total_available_tickets: ''
      },
      editShowForm: {
        id: '',
        name: '',
        place: '',
        date: '',
        price: '',
        city: '',
        country: '',
        total_available_tickets: ''
      },
      addArtistForm: {
        name: '',
        country: ''
      },
      removeArtistForm: {
        id: '',
        name: ''
      },
      show_to_modify: '',
      shows: []
    }
  },
  created () {
    this.getShows()
    this.logged = this.$route.query.logged
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged) {
      this.checkIsAdmin()
    }
    this.getMoneyAvailable()
  },
  methods: {
    buyTickets () {
      this.tickets_bought += 1
      this.money()
    },
    returnTickets () {
      this.remaining_tickets = this.total_tickets - this.tickets_bought
    },
    getMoneyAvailable () {
      if (this.money_total - (this.tickets_bought * this.price_event) < 0) {
        alert("You don't have enough money to make this purchase")
      }
      this.money_available = this.money_total - (this.tickets_bought * this.price_event)
    },
    decrementTicket (show) {
      this.count_items_added -= 1
      show.quantity -= 1
      if (show.quantity === 0) {
        this.deleteShowTickets(show)
      }
    },
    addShowToCart (show) {
      this.count_items_added += 1
      if (this.all_shows_id_added.has(show.id)) {
        show.quantity += 1
      } else {
        this.shows_added.push(show)
        show.quantity = 1
        this.all_shows_id_added.add(show.id)
      }
    },
    deleteShowTickets (show) {
      this.all_shows_id_added.delete(show.id)
      this.count_items_added -= show.quantity
      this.shows_added = this.shows_added.filter(function (value) {
        return value.id !== show.id
      })
    },
    addPurchase (parameters) {
      const path = `http://localhost:5000/orders/${this.username}`
      axios.post(path, parameters, {auth: {username: this.token}})
        .then(() => {
          console.log('Order done!')
          this.getShows()
          this.getMoneyAvailable()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getShows()
          this.getMoneyAvailable()
        })
      this.initForm()
    },
    finalizePurchase () {
      let parameters = []
      for (let i = 0; i < this.shows_added.length; i += 1) {
        parameters.push({
          id_show: this.shows_added[i].id,
          tickets_bought: this.tickets_bought[i]
        })
      }
      this.addPurchase(parameters)
      this.shows_added = []
      this.count_items_added = 0
      this.all_shows_id_added = new Set()
      this.getShows()
    },
    getShows () {
      const path = 'http://localhost:5000/shows'
      axios.get(path)
        .then((res) => {
          this.shows = res.data.shows
        })
        .catch((error) => {
          console.error(error)
        })
    },
    goToLogin () {
      this.$router.replace({path: '/userlogin', query: {}})
    },
    checkIsAdmin () {
      const path = `http://localhost:5000/account/` + this.username
      axios.get(path)
        .then((res) => {
          if (res.data.account.admin === 1) {
            this.is_admin = true
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    forgetUser () {
      this.logged = false
      this.username = ''
      this.token = ''
      this.is_admin = false
      this.money_available = 0
      this.$router.replace({path: '/', query: {}})
    },
    addShow (parameters) {
      const path = `http://localhost:5000/show`
      axios.post(path, parameters, {auth: {username: this.token}})
        .then(() => {
          console.log('Show added')
          this.getShows()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getShows()
        })
    },
    addArtist (parameters) {
      const path = `http://localhost:5000/artist`
      axios.post(path, parameters, {auth: {username: this.token}})
        .then(() => {
          console.log('Artist created!')
          this.addArtistInShow(parameters)
          this.getShows()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.addArtistInShow(parameters)
          this.getShows()
        })
    },
    addArtistInShow (parameters) {
      const path = `http://localhost:5000/show/${this.show_to_modify.id}/artist`
      axios.post(path, parameters, {auth: {username: this.token}})
        .then(() => {
          console.log('Artist added to show!')
          this.getShows()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getShows()
        })
      this.initForm()
    },
    removeArtistInShow (parameters) {
      const path = `http://localhost:5000/show/${this.show_to_modify.id}/artist/${this.removeArtistForm.id}`
      axios.delete(path, {auth: {username: this.token}})
        .then(() => {
          console.log('Artist deleted!')
          this.getShows()
        })
        .catch((error) => {
          console.log(error)
          this.getShows()
        })
      this.initForm()
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addShowModal.hide()
      const parameters = {
        place: this.addShowForm.place,
        name: this.addShowForm.name,
        city: this.addShowForm.city,
        country: this.addShowForm.country,
        date: this.addShowForm.date,
        price: this.addShowForm.price,
        total_available_tickets: this.addShowForm.total_available_tickets
      }
      this.addShow(parameters)
      this.initForm()
      this.getShows()
      this.show_modal_toggle = false
    },
    onReset (evt) {
      evt.preventDefault()
      this.initForm()
      this.show_modal_toggle = false
      this.$nextTick(() => {
        this.show_modal_toggle = true
      })
    },
    onSubmitAddArtistInShow (evt) {
      evt.preventDefault()
      this.$refs.addArtistModal.hide()
      const parameters = {
        name: this.addArtistForm.name,
        country: this.addArtistForm.country,
        disciplines: this.addArtistForm.genres
      }
      this.addArtist(parameters)
      this.initForm()
      this.getShows()
      this.show_modal_toggle = false
    },
    onResetAddArtistInShow (evt) {
      this.onReset(evt)
    },
    onSubmitRemoveArtistInShow (evt) {
      evt.preventDefault()
      this.$refs.deleteArtistModal.hide()
      const parameters = {
        name: this.removeArtistForm.name
      }
      this.removeArtistInShow(parameters)
      this.initForm()
      this.getShows()
      this.show_modal_toggle = false
    },
    onResetRemoveArtistInShow (evt) {
      this.onReset(evt)
    },
    updateShow (parameters) {
      const path = `http://localhost:5000/show/${this.editShowForm.id}`
      axios.put(path, parameters, {auth: {username: this.token}})
        .then(() => {
          console.log('Show Updated')
          this.getShows()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          alert('It was not possible to edit the show')
          this.getShows()
        })
      this.initForm()
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editShowModal.hide()
      const parameters = {
        id: this.editShowForm.id,
        name: this.editShowForm.name,
        price: this.editShowForm.price,
        date: this.editShowForm.date,
        country: this.editShowForm.country,
        city: this.editShowForm.city,
        place: this.editShowForm.place,
        total_available_tickets: this.editShowForm.total_available_tickets
      }
      this.updateShow(parameters)
      this.initForm()
      this.getShows()
      this.show_modal_toggle = false
    },
    removeShow (show) {
      let showid = show.id
      const path = `http://localhost:5000/show/${showid}`
      axios.delete(path, {auth: {username: this.token}})
        .then(() => {
          console.log('Orders done')
          this.initForm()
          this.getShows()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getShows()
        })
    },
    showFormNew () {
      this.show_modal_toggle = true
      this.$refs['addShowModal'].show()
    },
    showFormModify () {
      this.show_modal_toggle = true
      this.$refs['editShowModal'].show()
    },
    showFormAddArtist (show) {
      this.show_to_modify = show
      this.show_modal_toggle = true
      this.$refs['addArtistModal'].show()
    },
    showFormRemoveArtist (show) {
      this.show_to_modify = show
      this.show_modal_toggle = true
      this.$refs['removeArtistModal'].show()
    },
    initForm () {
      this.addShowForm.place = ''
      this.addShowForm.name = ''
      this.addShowForm.date = ''
      this.addShowForm.price = ''
      this.addShowForm.city = ''
      this.addShowForm.country = ''
      this.addShowForm.total_available_tickets = ''
      this.editShowForm.id = ''
      this.editShowForm.name = ''
      this.editShowForm.place = ''
      this.editShowForm.date = ''
      this.editShowForm.price = ''
      this.editShowForm.city = ''
      this.editShowForm.country = ''
      this.editShowForm.total_available_tickets = ''
      this.addArtistForm.name = ''
      this.addArtistForm.country = ''
      this.addArtistForm.genres = []
      this.removeArtistForm.id = ''
      this.removeArtistForm.name = ''
    }
  }
}
</script>
