// Displays a single review
export function createReviewCard(review){
    return `
     <div class="review-card">
       <strong> ${review.user}</strong>
       <p>${review.text} </p>
     </div>
     `;
}