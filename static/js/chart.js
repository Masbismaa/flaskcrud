document.addEventListener('DOMContentLoaded', () => {

    const canvas = document.getElementById('salesChart');
    if (!canvas || typeof Chart === 'undefined' || !window.salesChartData) return;

    const ctx = canvas.getContext('2d');

    // Gradient area di bawah garis (liquid fill)
    const areaGradient = ctx.createLinearGradient(0, 0, 0, canvas.height || 300);
    areaGradient.addColorStop(0, 'rgba(37, 99, 235, 0.35)');
    areaGradient.addColorStop(0.5, 'rgba(79, 70, 229, 0.12)');
    areaGradient.addColorStop(1, 'rgba(79, 70, 229, 0)');

    // Gradient garis
    const lineGradient = ctx.createLinearGradient(0, 0, canvas.width || 600, 0);
    lineGradient.addColorStop(0, '#2563eb');
    lineGradient.addColorStop(1, '#4f46e5');

    const labels = window.salesChartData.labels || [];
    const values = window.salesChartData.data || window.salesChartData.values || [];

    const salesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Omzet',
                data: values,
                fill: true,
                backgroundColor: areaGradient,
                borderColor: lineGradient,
                borderWidth: 3,
                tension: 0.45,
                pointRadius: 0,
                pointHoverRadius: 7,
                pointHoverBackgroundColor: '#ffffff',
                pointHoverBorderColor: '#2563eb',
                pointHoverBorderWidth: 3,
                pointHitRadius: 20,
                cubicInterpolationMode: 'monotone'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            animations: {
                x: {
                    type: 'number',
                    easing: 'easeInOutQuart',
                    duration: 1200,
                    from: NaN,
                    delay(ctx) {
                        return ctx.type === 'data' ? ctx.dataIndex * 60 : 0;
                    }
                },
                y: {
                    type: 'number',
                    easing: 'easeOutQuart',
                    duration: 900,
                    from: (ctx) => ctx.chart.scales.y.getPixelForValue(0)
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(255, 255, 255, 0.85)',
                    titleColor: '#374151',
                    bodyColor: '#1e293b',
                    bodyFont: { weight: '700' },
                    borderColor: 'rgba(37, 99, 235, 0.15)',
                    borderWidth: 1,
                    padding: 12,
                    cornerRadius: 14,
                    displayColors: false,
                    callbacks: {
                        label: (item) => {
                            const val = item.parsed.y || 0;
                            return 'Rp ' + val.toLocaleString('id-ID');
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#9ca3af', font: { size: 11 } }
                },
                y: {
                    grid: { color: 'rgba(148, 163, 184, 0.12)' },
                    border: { display: false },
                    ticks: {
                        color: '#9ca3af',
                        font: { size: 11 },
                        callback: (val) => 'Rp ' + (val / 1000) + 'k'
                    }
                }
            }
        }
    });

    window.addEventListener('resize', () => {
        salesChart.resize();
    });
});