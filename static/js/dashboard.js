document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/client_stats')
        .then(response => response.json())
        .then(data => {
            createStatusChart(data.status_data);
            createEmailsChart(data.email_data);
        });
});

function createStatusChart(statusData) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(statusData),
            datasets: [{
                data: Object.values(statusData),
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

function createEmailsChart(emailData) {
    const ctx = document.getElementById('emailsChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(emailData),
            datasets: [{
                data: Object.values(emailData),
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
