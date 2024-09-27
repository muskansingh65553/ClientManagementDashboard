// Main JavaScript file for common functionality

document.addEventListener('DOMContentLoaded', function() {
    // Add any common JavaScript functionality here
    console.log('Main JS loaded');
});

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.className = `fixed top-4 right-4 p-4 rounded-md text-white ${type === 'error' ? 'bg-red-500' : 'bg-green-500'}`;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
