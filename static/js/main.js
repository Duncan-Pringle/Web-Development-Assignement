// Dropdown 
function toggleDropdown() {
    const menu = document.getElementById("dropdown-menu");
    if (menu) {
        menu.classList.toggle("show");
    }
}

window.onclick = function(event) {
    if (!event.target.closest('#user-card')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            if (dropdowns[i].classList.contains('show')) {
                dropdowns[i].classList.remove('show');
            }
        }
    }
}

//  Generic watchlist toggle helper 
async function toggleWatchlistBtn(btn, endpoint) {
    try {
        const res  = await fetch(endpoint, { method: 'POST' });
        const data = await res.json();

        if (data.status === 'added') {
            btn.textContent = '✓ In Watchlist';
            btn.classList.add('btn-added');
        } else if (data.status === 'removed') {
            btn.textContent = '+ Add to Watchlist';
            btn.classList.remove('btn-added');
        } else if (res.status === 401) {
            window.location.href = '/login';
        }
    } catch (err) {
        console.error('Watchlist toggle failed:', err);
    }
}

// Movie watchlist button 
const movieWatchlistBtn = document.getElementById('watchlist-btn');
if (movieWatchlistBtn && movieWatchlistBtn.dataset.movieId) {
    movieWatchlistBtn.onclick = () => {
        const id = movieWatchlistBtn.dataset.movieId;
        toggleWatchlistBtn(movieWatchlistBtn, `/toggle-watchlist/${id}`);
    };
}

// TV show watchlist button 
const tvWatchlistBtn = document.getElementById('watchlist-btn');
if (tvWatchlistBtn && tvWatchlistBtn.dataset.showId) {
    tvWatchlistBtn.onclick = () => {
        const id = tvWatchlistBtn.dataset.showId;
        toggleWatchlistBtn(tvWatchlistBtn, `/toggle-tv-watchlist/${id}`);
    };
}


document.addEventListener('DOMContentLoaded', function() {
    const reviewBtn = document.getElementById('submit-review');
    
    if (reviewBtn) {
        reviewBtn.onclick = function() {
            const movieId = this.getAttribute('data-movie-id');
            const reviewInput = document.getElementById('review-text');
            const ratingInput = document.getElementById('review-rating');
            const msg = document.getElementById('review-msg');

            const text = reviewInput.value.trim();
            const rating = ratingInput.value;

            if (!text) {
                msg.innerText = "Please write a review!";
                msg.style.color = "#e74c3c";
                return;
            }

            fetch(`/post-review/${movieId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    reviewText: text,
                    rating: rating 
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    msg.innerText = "✅ Review & Rating saved!";
                    msg.style.color = "#4CAF50";
                    reviewInput.value = ""; // Clear the text area
                } else {
                    msg.innerText = "❌ Error saving review.";
                    msg.style.color = "#e74c3c";
                }
            })
            .catch(err => {
                console.error("Review error:", err);
                msg.innerText = "Connection error.";
            });
        };
    }
});