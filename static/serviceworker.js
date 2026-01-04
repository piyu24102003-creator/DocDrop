// Minimal Service Worker to enable 'Add to Home Screen'
self.addEventListener('install', (event) => {
    console.log('Service Worker installed');
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker activated');
});

self.addEventListener('fetch', (event) => {
    // Simple pass-through for now. 
    // In the future, implement caching here for offline support.
});
