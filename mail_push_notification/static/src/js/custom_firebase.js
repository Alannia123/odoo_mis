/** @odoo-module **/

// Check if Firebase is available
if (typeof firebase === "undefined") {
    console.error("❌ Firebase SDK not loaded. Check your assets.xml.");
}



// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyDyUYACtVsZy14L5IEkpIc_gGKTq9AJ8yY",
    authDomain: "mis-odoo-98a36.firebaseapp.com",
    projectId: "mis-odoo-98a36",
    storageBucket: "mis-odoo-98a36.firebasestorage.app",
    messagingSenderId: "526211843962",
    appId: "1:526211843962:web:69ae06d2bf93bf917338c3"
};

// Initialize Firebase (Ensure it's only initialized once)
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

// Firebase Messaging
const messaging = firebase.messaging();

async function requestNotificationPermission() {
    try {
        const permission = await Notification.requestPermission();
        if (permission === "granted") {
            const token = await messaging.getToken();
            console.log("✅ Firebase Token:", token);

            // Send token to Odoo backend
            await fetch('/store_firebase_token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token })
            });
        } else {
            console.warn("❌ Notification permission denied");
        }
    } catch (error) {
        console.error("❌ Error getting permission:", error);
    }
}

// Handle incoming messages
messaging.onMessage((payload) => {
    console.log("📩 Notification received:", payload);
    new Notification(payload.notification.title, {
        body: payload.notification.body,
        icon: payload.notification.icon
    });
});

// Call the function to request permission
requestNotificationPermission();
