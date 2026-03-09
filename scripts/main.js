import {API} from "./api.js";
import {state} from "./state.js";

import {renderLogin} from "./loginView.js";
import {renderAdmin} from "./adminView.js";
import {renderMovie} from "./movieView.js";

import {createReviewCard} from "./reviewCard.js";
import {createFeaturedCard,createPosterCard,createPopularSection} from  "./skeleton.js"
const mainContainer =document.getElementById("main-card");

// Home Page
async function loadHome() {

    try{
       const movies= [
       {t:"Movie 1"},
       {t:"Movie 2"},
       {t:"Movie 3"},
       {t:"Movie 4"},
       {t:"Movie 5"}];
        const featured= createFeaturedCard(movies[0]);
        const posters= movies.slice(1,6)
        .map(t=> createPosterCard(t.title))
        .join("");

        const popular = createPopularSection(posters);
        mainContainer.innerHTML= featured + popular;

    }

    catch{
       mainContainer.innerHTML="<p>Error Occured. Movies can't be loaded.</p>";
    }
    
}

// Login Page

function showLogin(){
    mainContainer.innerHTML= renderLogin();
    document.getElementById("submitLogin").onclick= async ()=>{
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      const user= await API.login({username,password});
      state.user= user;

      if(user.role==="admin"){
        loadAdmin();
      }
      else{
        loadHome();
      }
    };
}

// Admin Dashboard
async function loadAdmin() {
    mainContainer.innerHTML = renderAdmin();

    try{
       const reviews= await fetch ("/api/admin/reviews");
       const reviewData= await reviews.json();
       const reviewList= document.getElementById("reviewAdminList");
      
       reviewData.forEach(e => {
        
        reviewList.innerHTML += `
          <div>
          ${e.text}

         <button onclick="deleteReview(${e.id})">
          Delete
         </button>
        `;
       });
        
    }

    catch{}
    
}

// Delete Review 
window.deleteReview= async function (id) {
    
    await fetch (`/api/admin/review/${id}`,{
        method: "DELETE"
    }

    );

    loadAdmin();
};

// Movie Details
window.loadMovie = async function (id) {
    
    const movie= await API.movie(id);
    mainContainer.innerHTML= renderMovie(movie);
    document.getElementById("backButton").onclick= loadHome;

    const reviews= await API.reviews(id);
    const list= document.getElementById("reviewList");

    reviews.forEach(e=> {
        list.innerHTML += createReviewCard(e);
    });

    document.getElementById("submitReview").onclick= async ()=>{
       const text= document.getElementById("reviewText").value;
       await API.addReview({movieId:id,text});
       loadMovie(id);
    };

};

// Search
document.getElementById("searchInput")
    .addEventListener("keypress", async x=>{

      if (x.key==="Enter"){
        const movies= await API.search(x.target.value);
        const posters= movies
        .map(e=>createPosterCard(e.title))
        .join("");

        mainContainer.innerHTML=createPopularSection(posters); }
    }

    );

    // Navigation
    document.getElementById("homeNavigation").onclick=loadHome;
    document.getElementById("loginButton").onclick=showLogin;

    // Intitial page
    loadHome();