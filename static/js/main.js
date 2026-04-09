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

document.addEventListener('DOMContentLoaded', function() {
    const watchlistBtn = document.getElementById('watchlist-btn');
    if (watchlistBtn) {
        watchlistBtn.addEventListener('click', function() {
            const btn = this;
            const movieId = btn.getAttribute('data-movie-id');
            console.log('Testing', movieId); // Debugging log
            // If movieId is missing, stop here
            if (!movieId) return;

            fetch(`/toggle-watchlist/${movieId}`, { method: 'POST' })
            .then(response => {
                if (response.status === 401) {
                    alert("Please log in to use the watchlist!");
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (!data) return;
                
                if (data.status === 'added') {
                    btn.innerText = '✓ In Watchlist';
                    btn.classList.add('btn-added');
                } else if (data.status === 'removed') {
                    btn.innerText = '+ Add to Watchlist';
                    btn.classList.remove('btn-added');
                }
            })
            .catch(err => console.error('Error:', err));
        });
    }
});