// scripts/skeleton.js

export const createFeaturedCard = (data) => {
    return `
        <section class="featured-section">
            <h2>${data.title}</h2>
            <div class="featured-content">
                <div class="image-placeholder featured-img">Image Placeholder</div>
                <div class="featured-details">
                    <p class="synopsis">${data.description}</p>
                    <div class="button-group">
                        <button class="btn">Watch Trailer</button>
                        <button class="btn">Details</button>
                    </div>
                </div>
            </div>
        </section>
    `;
};

export const createPosterCard = (title) => {
    return `
        <div class="poster-item">
            <div class="image-placeholder poster-img">Poster</div>
            <p class="poster-title">${title}</p>
        </div>
    `;
};

export const createPopularSection = (postersHtml) => {
    return `
        <section class="popular-section">
            <h2>Popular Movies/Shows</h2>
            <div class="poster-grid">
                ${postersHtml}
            </div>
        </section>
    `;
};