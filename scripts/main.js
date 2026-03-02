import { createFeaturedCard, createPosterCard, createPopularSection } from './skeleton.js';

const mainContainer = document.getElementById('main-card');

//Mock Data
const featuredData = {
    title: "Featured Movie/Show Title",
    description: "Short synopsis or description of the featured movie/show. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
};

const popularTitles = ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"];

// UI
function renderApp() {
    // Generate Featured Section
    const featuredHtml = createFeaturedCard(featuredData);

    // Generate Popular Section Grid
    const postersHtml = popularTitles
        .map(title => createPosterCard(title))
        .join('');
    
    const popularHtml = createPopularSection(postersHtml);

    // Inject into DOM
    mainContainer.innerHTML = featuredHtml + popularHtml;
}

// Run render
renderApp();