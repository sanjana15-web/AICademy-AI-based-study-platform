// wait until page loads
document.addEventListener("DOMContentLoaded", function(){

let isLoggedIn = localStorage.getItem("loggedIn") === "true";

// ===== SIDEBAR =====

window.toggleMenu = function(){
document.getElementById("sidebar").classList.toggle("show");
}


// ===== LOGIN MODAL =====

window.openLoginModal = function(){

let modal = document.createElement("div");

modal.className = "login-modal";

modal.innerHTML = `
<div class="login-box">

<h2>Login</h2>

<input type="email" id="email" placeholder="Enter Email">

<input type="password" id="password" placeholder="Enter Password">

<button id="loginSubmit">Login</button>

<p id="closeLogin">Cancel</p>

</div>
`;

document.body.appendChild(modal);


// close login
document.getElementById("closeLogin").onclick = function(){
modal.remove();
};
 

// submit login
document.getElementById("loginSubmit").onclick = function(){

let email = document.getElementById("email").value;
let password = document.getElementById("password").value;

let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if(!emailPattern.test(email)){
alert("Please enter a valid email");
return;
}
if(password.length < 6){
alert("Please enter a password with at least 6 characters");
return;
}

localStorage.setItem("loggedIn","true");
isLoggedIn = true;

modal.remove();

alert("Login Successful!");

};

}


// ===== LOGIN CHECK =====

function requireLogin(){

if(!isLoggedIn){
openLoginModal();
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

openLoginModal();

});

}

});