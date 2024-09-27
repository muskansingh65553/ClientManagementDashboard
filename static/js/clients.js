document.addEventListener('DOMContentLoaded', function() {
    const clientTable = document.getElementById('clientTable');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const reminderForm = document.getElementById('reminderForm');

    if (clientTable && searchInput && statusFilter) {
        searchInput.addEventListener('input', filterClients);
        statusFilter.addEventListener('change', filterClients);
    }

    if (reminderForm) {
        reminderForm.addEventListener('submit', setReminder);
    }
});

function filterClients() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const rows = document.querySelectorAll('#clientTable tbody tr');

    rows.forEach(row => {
        const companyName = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
        const contactName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        const status = row.querySelector('td:nth-child(5)').textContent;

        const matchesSearch = companyName.includes(searchTerm) || contactName.includes(searchTerm);
        const matchesStatus = statusFilter === '' || status === statusFilter;

        row.style.display = matchesSearch && matchesStatus ? '' : 'none';
    });
}

function deleteClient(clientId) {
    if (confirm('Are you sure you want to delete this client?')) {
        fetch(`/delete_client/${clientId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrf_token')
            }
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                showNotification('Error deleting client', 'error');
            }
        });
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function showReminderModal(clientId) {
    document.getElementById('clientId').value = clientId;
    document.getElementById('reminderModal').classList.remove('hidden');
}

function closeReminderModal() {
    document.getElementById('reminderModal').classList.add('hidden');
}

function setReminder(event) {
    event.preventDefault();
    const clientId = document.getElementById('clientId').value;
    const reminderDate = document.getElementById('reminderDate').value;
    const reminderMessage = document.getElementById('reminderMessage').value;

    fetch(`/set_reminder/${clientId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrf_token')
        },
        body: `reminder_date=${reminderDate}&reminder_message=${reminderMessage}`
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Reminder set successfully', 'success');
            closeReminderModal();
            location.reload();
        } else {
            showNotification('Error setting reminder', 'error');
        }
    });
}
