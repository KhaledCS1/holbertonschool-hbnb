// Base URL for the API
const apiBase = 'http://localhost:5000/api';

// Utility to get a cookie's value
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Check authentication and control login link
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!loginLink) return;
  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// Fetch places from API
async function fetchPlaces(token) {
  try {
    const res = await fetch(`${apiBase}/places`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const places = await res.json();
      populatePriceFilter(places);
      displayPlaces(places);
    } else {
      console.error('Failed to fetch places');
    }
  } catch (err) {
    console.error('Network error fetching places', err);
  }
}

// Populate price filter options
function populatePriceFilter(places) {
  const select = document.getElementById('price-filter');
  const prices = [10, 50, 100];
  prices.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p;
    opt.textContent = `$${p}`;
    select.appendChild(opt);
  });
  const allOpt = document.createElement('option');
  allOpt.value = 'All';
  allOpt.textContent = 'All';
  select.appendChild(allOpt);

  // Attach filter event
  select.addEventListener('change', () => filterPlaces(places));
}

// Render places into DOM
function displayPlaces(places) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';
  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = place.price_per_night;
    div.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description}</p>
      <p>Location: ${place.city}, ${place.country}</p>
      <p>Price: $${place.price_per_night}</p>
    `;
    container.appendChild(div);
  });
}

// Filter places by selected price
function filterPlaces(places) {
  const max = document.getElementById('price-filter').value;
  const cards = document.querySelectorAll('.place-card');
  cards.forEach(card => {
    const price = parseFloat(card.dataset.price);
    if (max === 'All' || price <= parseFloat(max)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
});