function toggleDropdown() {
    document.getElementById("dropdown-menu").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.closest('#user-card')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function movieDetails() {
    window.location.href = "/movie/0";
}

document.getElementById('watchlist-btn').addEventListener('click', function() {
    const btn = this;
    const movieId = btn.getAttribute('data-movie-id');

    fetch(`/toggle-watchlist/${movieId}`, { method: 'POST' })
    .then(response => {
        if (response.status === 401) {
            alert("Please log in to use the watchlist!");
            return;
        }
        return response.json();
    })
    .then(data => {
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