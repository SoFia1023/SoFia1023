// Basic service worker file
// This empty service worker file will prevent 404 errors in the browser console

self.addEventListener('install', function(event) {
  // Perform install steps
  console.log('Service Worker installed');
});

self.addEventListener('activate', function(event) {
  console.log('Service Worker activated');
});

// No fetch handler - will use browser default fetch behavior
