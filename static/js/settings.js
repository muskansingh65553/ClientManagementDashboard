document.addEventListener('DOMContentLoaded', function() {
    const settingsForm = document.getElementById('settingsForm');
    if (settingsForm) {
        settingsForm.addEventListener('submit', updateProfile);
    }
});

function updateProfile(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/settings', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            showNotification('Profile updated successfully', 'info');
        } else {
            showNotification('Error updating profile', 'error');
        }
    });
}
