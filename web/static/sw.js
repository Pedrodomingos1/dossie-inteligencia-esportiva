const CACHE_NAME = 'dossie-esportivo-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css',
    '/static/icons/icon.svg',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Cacheando shell do app');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

// Ativação e limpeza de caches antigos
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Ativando...');
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    console.log('[Service Worker] Removendo cache antigo', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    return self.clients.claim();
});

// Interceptação de requisições
self.addEventListener('fetch', (event) => {
    // Ignora requisições não-GET
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then((response) => {
            // Retorna do cache se disponível
            if (response) {
                return response;
            }
            // Caso contrário, busca na rede
            return fetch(event.request).then((networkResponse) => {
                // Opcional: Cachear dinamicamente novas requisições GET bem-sucedidas
                // return caches.open(CACHE_NAME).then((cache) => {
                //     cache.put(event.request, networkResponse.clone());
                //     return networkResponse;
                // });
                return networkResponse;
            });
        })
    );
});
