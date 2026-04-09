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

const watchlistbtn = document.getElementById('watchlist-btn');

watchlistbtn.onclick = async () => {
    const id = watchlistbtn.dataset.movieId;

    const res = await fetch(`/toggle-watchlist/${id}`, {
        method: 'POST'
    });

    const data = await res.json();

    if (data.status === 'added') {
        watchlistbtn.textContent = '✓ In Watchlist';
        watchlistbtn.classList.add('added');
    } else {
        watchlistbtn.textContent = '+ Add to Watchlist';
        watchlistbtn.classList.remove('added');
    }
};