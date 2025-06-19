// static/sw.js
const CACHE_NAME = 'my-streamlit-app-cache-v1';
const urlsToCache = [
  '/',
  // ここにキャッシュしたい他のリソース（CSS, JSファイルなど）を追加できますが、
  // Streamlitでは動的に生成されるため、ルート'/'のキャッシュが基本となります。
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // キャッシュがあればそれを返す
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
