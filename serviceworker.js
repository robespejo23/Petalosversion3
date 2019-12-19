//instalacion y intersectacion

var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/core/css/estilo_flores.css',
    '/static/core/img/petalos.jpg',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
       fetch(event.request)
       .then(function(result){
           return caches.open(CACHE_NAME)
           .then(function(c){
               c.put(event.request.url, result.clone());
               return result;
           })
       })
       .catch(function(e){
           return caches.match(event.request)
       })
    );
});

importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');



var firebaseConfig = {
    apiKey: "AIzaSyAKVGabWOKFBXbM7vxTtlLpbp9StsJlvIg",
    authDomain: "flore-5b7ed.firebaseapp.com",
    databaseURL: "https://flore-5b7ed.firebaseio.com",
    projectId: "flore-5b7ed",
    storageBucket: "flore-5b7ed.appspot.com",
    messagingSenderId: "64904305891",
    appId: "1:64904305891:web:f8ebfb6fd45ed714b579d6",
    measurementId: "G-M92Z6EGCX3"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){

    let title = payload.notificacion.title;
   
        let options = {
            body:payload.notificacion.body,
            icon:payload.notificacion.icon,

        }

        self.registration.shownotification(title, options);
})