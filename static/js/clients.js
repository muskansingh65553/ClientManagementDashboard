document.addEventListener('DOMContentLoaded', function() {
    const clientTable = document.getElementById('clientTable');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');

    if (clientTable && searchInput && statusFilter) {
        searchInput.addEventListener('input', filterClients);
        statusFilter.addEventListener('change', filterClients);
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
