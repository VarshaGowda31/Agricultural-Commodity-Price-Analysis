document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('priceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Sample Price Trend',
                data: [2200, 2500, 2100, 2700, 3000, 2600],
                backgroundColor: 'rgba(0, 255, 204, 0.2)',
                borderColor: '#00ffcc',
                borderWidth: 3,
                pointBackgroundColor: '#00ffcc',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#00ffcc'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: '#fff'
                    }
                },
                x: {
                    ticks: {
                        color: '#fff'
                    }
                }
            }
        }
    });
});
