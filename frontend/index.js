//Packages
const express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
const app = express();
const axios = require("axios");
const port = 3000;
// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
//setup public folder
app.use(express.static("./public"));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());

//Home page
app.get("/", function (req, res) {
  res.render("pages/home");
});

//Login Page
app.post("/login_page", function (req, res) {
  const { username, password } = req.body;

  if (username === "username" && password === "password") {
    res.redirect("/current_cargo");
  } else {
    res.redirect("/");
  }
});
// View Current Cargo
app.get("/current_cargo", function (req, res) {
  //GET Request to API to get the cargo data
  axios.get("http://127.0.0.1:5000/cargo").then((response) => {
    cargosData = response.data[0];
    //If showArrived is on, meaning if the checkbox is checked
    showArrived = req.query.showArrived === "on";
    filteredCargos = cargosData.filter((cargo) => {
      return (
        // checkbox is checked and arrival value is not null
        (showArrived && cargo.arrival !== null) ||
        new Date(cargo.arrival) > new Date()
      );
    });
    // Render the cargostatus page to display the data
    res.render("pages/cargostatus", {
      cargos: filteredCargos,
      showArrived: showArrived,
    });
  });
});
// View Spaceships
app.get("/spaceship", function (req, res) {
  axios.get("http://127.0.0.1:5000/spaceship").then((response) => {
    spaceship = response.data[0]; // Get the JSON data into spaceship
    res.render("pages/spaceships", {
      spaceships: spaceship,
    });
  });
});
// Add Spaceships
app.post("/add_spaceship", function (req, res) {
  // Get maxweight and captainid from the text input
  maxWeight = req.body.maxweight;
  captainId = req.body.captainid;
  axios
    .post("http://127.0.0.1:5000/spaceship", {
      maxweight: maxWeight,
      captainid: captainId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/spaceship");
    });
});

// Update Spaceship
app.post("/update_spaceship/:id", function (req, res) {
  id = req.params.id; //Get the id from the URL
  maxWeight = req.body.maxweight;
  captainId = req.body.captainid;
  axios
    // Insert the input id into URL and request from python code
    .put(`http://127.0.0.1:5000/spaceship/${id}`, {
      maxweight: maxWeight,
      captainid: captainId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/spaceship");
    });
});

// Delete Spaceship
app.post("/delete_spaceship/:id", function (req, res) {
  id = req.params.id; // Get the ID from URl
  axios.delete(`http://127.0.0.1:5000/spaceship/${id}`).then((response) => {
    console.log(id);
    res.redirect("/spaceship"); // Redirecting to same page after the button is clicked
  });
});

// View Cargo
app.get("/cargo", function (req, res) {
  axios.get("http://127.0.0.1:5000/cargo").then((response) => {
    cargo = response.data[0];
    // Render cargo EJS page
    res.render("pages/cargo", {
      cargos: cargo,
    });
  });
});
// Add Cargo
app.post("/add_cargo", function (req, res) {
  // Input from the text fields
  weight = req.body.weight;
  cargotype = req.body.cargotype;
  shipId = req.body.shipid;

  axios
    // Making POST Request to add new cargo in the SQL Database
    .post("http://127.0.0.1:5000/cargo", {
      weight: weight,
      cargotype: cargotype,
      shipid: shipId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/cargo");
    });
});

// Update Cargo
app.post("/update_cargo/:id", function (req, res) {
  id = req.params.id;
  weight = parseFloat(req.body.weight); // Converting to float because it is comparing with another float value in the backend python code
  cargotype = req.body.cargotype;
  departure = req.body.departure;
  arrival = req.body.arrival;
  shipId = req.body.shipid;
  axios
    // Making Put (Update) Request
    .put(`http://127.0.0.1:5000/cargo/${id}`, {
      weight: weight,
      cargotype: cargotype,
      departure: departure,
      arrival: arrival,
      shipid: shipId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/cargo"); // Redirecting to cargo page (same page) after clicking update
    });
});

// Delete Cargo
app.post("/delete_cargo/:id", function (req, res) {
  id = req.params.id;
  axios.delete(`http://127.0.0.1:5000/cargo/${id}`).then((response) => {
    console.log(id);
    res.redirect("/cargo");
  });
});

// View Captain
app.get("/captain", function (req, res) {
  axios.get("http://127.0.0.1:5000/captain").then((response) => {
    captain = response.data[0];
    res.render("pages/captain", {
      captains: captain,
    });
  });
});
// Add Captain
app.post("/add_captain", function (req, res) {
  // Getting the input from the text fields into variables
  firstname = req.body.firstname;
  lastname = req.body.lastname;
  homeplanet = req.body.homeplanet;
  captain_rank = req.body.captain_rank;
  axios
    .post("http://127.0.0.1:5000/captain", {
      firstname: firstname,
      lastname: lastname,
      homeplanet: homeplanet,
      captain_rank: captain_rank,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/captain");
    });
});

// Update Captain
app.post("/update_captain/:id", function (req, res) {
  id = req.params.id;
  firstname = req.body.firstname;
  lastname = req.body.lastname;
  homeplanet = req.body.homeplanet;
  captain_rank = req.body.captain_rank;
  axios
    .put(`http://127.0.0.1:5000/captain/${id}`, {
      firstname: firstname,
      lastname: lastname,
      homeplanet: homeplanet,
      captain_rank: captain_rank,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/captain");
    });
});

// Delete Captain
app.post("/delete_captain/:id", function (req, res) {
  id = req.params.id;
  axios.delete(`http://127.0.0.1:5000/captain/${id}`).then((response) => {
    console.log(id);
    res.redirect("/captain");
  });
});

app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));
