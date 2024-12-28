document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("chartLoader");
    const chartCanvas = document.getElementById("bloodPressureChart");

    const urlParams = new URLSearchParams(window.location.search);
    const range = urlParams.get('range') || 'last_week'; // Default to 'last_week'

    fetch(`/blood_pressure/data?range=${range}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                loader.textContent = "Failed to load data.";
                return;
            }

            const labels = data.map(record => record.date.replace('T', ' '));
            const systolic = data.map(record => record.systolic);
            const diastolic = data.map(record => record.diastolic);
            const pulse = data.map(record => record.pulse);

            const ctx = chartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Systolic (mmHg)',
                            data: systolic,
                            borderColor: 'hsl(183, 47%, 49%)',
                            backgroundColor: 'hsla(183, 47%, 49%, 0.2)',
                            borderWidth: 2,
                            tension: 0.4
                        },
                        {
                            label: 'Diastolic (mmHg)',
                            data: diastolic,
                            borderColor: 'hsl(338, 71%, 68%)',
                            backgroundColor: 'hsla(338, 71%, 68%, 0.2)',
                            borderWidth: 2,
                            tension: 0.4
                        },
                        {
                            label: 'Pulse (bpm)',
                            data: pulse,
                            borderColor: 'hsl(39, 84%, 48%)',
                            backgroundColor: 'hsla(39, 84%, 48%, 0.2)',
                            borderWidth: 2,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `${context.dataset.label}: ${context.parsed.y}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Value'
                            }
                        }
                    }
                }
            });

            loader.classList.add("d-none");
            chartCanvas.classList.remove("d-none");
        })
        .catch(error => {
            console.error('Error fetching blood pressure data:', error);
        });
});
