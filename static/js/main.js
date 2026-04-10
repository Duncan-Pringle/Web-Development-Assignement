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
