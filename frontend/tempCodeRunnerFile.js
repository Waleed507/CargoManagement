const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;
const axios = require("axios");

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

//setup public folder
app.use(express.static("./public"));

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// parse application/json
app.use(bodyParser.json());

let isAuthenticated = false;

app.get("/", function (req, res) {
  res.render("pages/home");
});

app.post("/home", function (req, res) {
  var user = req.body.username;
  var password = req.body.password;
  isAuthenticated = user === "admin" && password === "password";

  if (isAuthenticated) {
    res.render("pages/form");
  } else {
    req.flash("error", "Invalid username or password");
    res.redirect("/");
  }
});

app.get("/form", function (req, res) {
  if (isAuthenticated) {
    res.render("pages/form");
  } else {
    req.flash("error", "You must be logged in to access this page");
    res.redirect("/");
  }
});

app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));
