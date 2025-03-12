// Minimal service worker file
// This service worker does nothing but register itself

self.addEventListener('install', function(event) {
  // Skip waiting to activate immediately
  self.skipWaiting();
  console.log('Service Worker installed');
});

self.addEventListener('activate', function(event) {
  // Claim clients to take control immediately
  event.waitUntil(clients.claim());
  console.log('Service Worker activated');
});

// No fetch handler - will use browser default fetch behavior
