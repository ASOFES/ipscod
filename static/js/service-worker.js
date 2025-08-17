self.addEventListener('push', function(event) {
    let data = {};
    if (event.data) {
        data = event.data.json();
    }
    const title = data.title || 'Notification';
    const options = {
        body: data.body || '',
        icon: data.icon || '/static/images/logo_ips_co.png',
        badge: data.badge || '/static/images/logo_ips_co.png',
        data: data.url || '/',
    };
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    const url = event.notification.data || '/';
    event.waitUntil(
        clients.matchAll({ type: 'window' }).then(function(clientList) {
            for (var i = 0; i < clientList.length; i++) {
                var client = clientList[i];
                if (client.url === url && 'focus' in client)
                    return client.focus();
            }
            if (clients.openWindow) {
                return clients.openWindow(url);
            }
        })
    );
}); 