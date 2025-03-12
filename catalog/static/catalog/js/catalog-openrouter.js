/**
 * JavaScript for the OpenRouter-inspired catalog page
 */

// Get Django variables from data attributes
const djangoData = document.getElementById('django-data');
const isAuthenticated = djangoData.dataset.isAuthenticated === 'true';
const loginUrl = djangoData.dataset.loginUrl;
const currentPath = djangoData.dataset.currentPath;
const catalogUrl = djangoData.dataset.catalogUrl;

document.addEventListener('DOMContentLoaded', function() {
  // Handle search input
  const searchInput = document.getElementById('search-input');
  let searchTimeout;
  
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(function() {
        applyFilters();
      }, 500);
    });
  }
  
  // Handle radio button changes
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  radioButtons.forEach(function(radio) {
    radio.addEventListener('change', function() {
      applyFilters();
    });
  });
  
  // Apply filters function
  function applyFilters() {
    const searchQuery = searchInput.value.trim();
    const category = document.querySelector('input[name="category"]:checked').value;
    const pricing = document.querySelector('input[name="pricing"]:checked').value;
    const sort = document.querySelector('input[name="sort"]:checked').value;
    
    let url = catalogUrl + '?';
    if (searchQuery) url += `q=${encodeURIComponent(searchQuery)}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    if (pricing) url += `pricing=${encodeURIComponent(pricing)}&`;
    if (sort) url += `sort=${encodeURIComponent(sort)}&`;
    
    // Remove trailing & if exists
    if (url.endsWith('&')) {
      url = url.slice(0, -1);
    }
    
    window.location.href = url;
  }
});

/**
 * Toggle favorite function
 */
function toggleFavorite(event, aiId) {
  event.preventDefault();
  event.stopPropagation();
  
  if (isAuthenticated) {
    // User is authenticated, make API call
    fetch('/catalog/ai/' + aiId + '/favorite/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      }
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
      const favoriteBtn = event.currentTarget;
      const favoriteIcon = favoriteBtn.querySelector('i');
      
      if (data.is_favorite) {
        favoriteIcon.classList.remove('far');
        favoriteIcon.classList.add('fas');
        favoriteBtn.setAttribute('title', 'Remove from favorites');
      } else {
        favoriteIcon.classList.remove('fas');
        favoriteIcon.classList.add('far');
        favoriteBtn.setAttribute('title', 'Add to favorites');
      }
    })
    .catch(function(error) {
      console.error('Error toggling favorite:', error);
    });
  } else {
    // User is not authenticated, redirect to login
    window.location.href = loginUrl + '?next=' + currentPath;
  }
}

/**
 * Helper function to get CSRF token
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
