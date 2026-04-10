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

// Watchlist button 
const watchlistBtn = document.getElementById('watchlist-btn');

if (watchlistBtn) {
    watchlistBtn.onclick = async () => {
        const id = watchlistBtn.dataset.movieId;

        try {
            const res = await fetch(`/toggle-watchlist/${id}`, {
                method: 'POST'
            });

            const data = await res.json();

            if (data.status === 'added') {
                watchlistBtn.textContent = '✓ In Watchlist';
                watchlistBtn.classList.add('btn-added');  // only add btn-added, never remove btn
            } 
            else if (data.status === 'removed') {
                watchlistBtn.textContent = '+ Add to Watchlist';
                watchlistBtn.classList.remove('btn-added');  // only remove btn-added, keep btn always
            } 
            else if (data.status === 'error' && res.status === 401) {
        
                window.location.href = '/login';
            }
        } 
        catch (err) {
            console.error('Watchlist toggle failed:', err);
        }
    };
}
