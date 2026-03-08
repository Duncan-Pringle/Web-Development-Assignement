// Movie details page 
export function renderMovie(){
    return `
    <div class="view">
    <button id="backButton">Back</button>
    <h2> ${movie.title}</h2>
    <p>${movie.overview}</p>
    <h3>Reviews</h3>
    <div id="reviewList"></div>
    <textarea id="reviewText"></textarea>
    <button id="submitReview">Submit Review</button>
    `;
}