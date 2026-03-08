// Manages all backend API requests 
async function request(url, options={}) {
    const response = await fetch (url,options);

    if (! response.ok){
       throw new Error("API request failed");
    }
    return response.json();
}

export const API= {
    // Popular movies
    popular: () => request ("/api/popular"),

    //Search movies
    search: (query) => request (`/api/search?q=${query}`),

    // Login request 
     login:(data) =>
      request ("/api/login",{
      method : "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(data)
    }),

    //Get movie details 
    movie:(id)=>request(`/api/movie/${id}`),

    //Movie reviews
    reviews:(id)=>request(`/api/reviews/${id}`),

    //Add review
    addReview:(data)=>
        request ("/api/review",{
          method:"POST",
          headers:{"Content-Type":"application/json"},
          body:JSON.stringify(data)
        })

};