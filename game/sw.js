var VERSION = "nae-foundation-1";
var CORE = [
  "./",
  "./index.html",
  "./manifest.json",
  "./css/game.css",
  "./js/app.mjs",
  "./js/engine.mjs",
  "./js/art.mjs",
  "./data/cards.json",
  "./data/daily-verses.json",
  "./assets/title.svg",
  "./assets/icon.svg",
  "./fonts/LilitaOne-Regular.ttf",
  "./fonts/Kanit-Regular.ttf",
  "./fonts/Kanit-Medium.ttf"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(VERSION).then(function (cache) {
      return cache.addAll(CORE);
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (key) { return key !== VERSION; }).map(function (key) {
        return caches.delete(key);
      }));
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener("fetch", function (event) {
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.indexOf("/audio/") !== -1) {
    event.respondWith(fetch(event.request).catch(function () {
      return new Response("", { status: 404 });
    }));
    return;
  }
  event.respondWith(
    caches.match(event.request).then(function (hit) {
      return hit || fetch(event.request);
    })
  );
});
