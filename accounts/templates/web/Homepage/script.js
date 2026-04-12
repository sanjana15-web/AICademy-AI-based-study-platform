// wait until page loads
document.addEventListener("DOMContentLoaded", function(){

let isLoggedIn = localStorage.getItem("loggedIn") === "true";


// ===== SIDEBAR =====

window.toggleMenu = function(){
document.getElementById("sidebar").classList.toggle("show");
}


// ===== LOGIN REDIRECT =====
function goToLogin(){
window.location.href = "login.html";   // same tab (best)
}


// ===== LOGIN CHECK =====

function requireLogin(){

if(!isLoggedIn){
goToLogin();   // redirect instead of popup
return false;
}

return true;

}


// ===== FEATURE CARDS =====
document.querySelectorAll(".feature-card").forEach(card=>{

card.addEventListener("click",function(){

if(!requireLogin()) return;

alert("Tool will open here.");

});

});


// ===== PRICING BUTTONS =====
document.querySelectorAll(".price-card button").forEach(btn=>{

btn.addEventListener("click",function(){

if(!requireLogin()) return;

alert("Plan activated!");

});

});


// ===== HERO BUTTON =====
let heroBtn = document.querySelector(".try-btn");

if(heroBtn){

heroBtn.addEventListener("click",function(){

if(!requireLogin()) return;

alert("Opening AI Tools");

});

}


// ===== LOGIN BUTTON =====
let loginBtn = document.querySelector(".login-btn button");

if(loginBtn){

loginBtn.addEventListener("click",function(){

goToLogin();   // redirect to login page

});

}

});