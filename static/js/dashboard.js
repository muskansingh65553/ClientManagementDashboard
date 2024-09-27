document.addEventListener('DOMContentLoaded', function() {
    // Fetch client data and create charts
    fetch('/api/clients')
        .then(response => response.json())
        .then(data => {
            createStatusChart(data);
            createEmailsChart(data);
        });
});

function createStatusChart(clients) {
    const statusCounts = {};
    clients.forEach(client => {
        statusCounts[client.status] = (statusCounts[client.status] || 0) + 1;
    });

    const ctx = document.getElementById('statusChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(statusCounts),
            datasets: [{
                data: Object.values(statusCounts),
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF'
                ]
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Client Status Distribution'
            }
        }
    });
}

function createEmailsChart(clients) {
    const emailCounts = {
        'With Email': clients.filter(client => client.email).length,
        'Without Email': clients.filter(client => !client.email).length
    };

    const ctx = document.getElementById('emailsChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(emailCounts),
            datasets: [{
                data: Object.values(emailCounts),
                backgroundColor: [
                    '#36A2EB',
                    '#FF6384'
                ]
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Clients with/without Email'
            }
        }
    });
}
