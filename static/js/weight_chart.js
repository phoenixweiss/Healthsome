document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("chartLoader");
    const chartCanvas = document.getElementById("weightChart");

    // Extract the selected range from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const range = urlParams.get('range') || 'last_week'; // Default to 'last_week'

    // Fetch data for the selected range
    fetch(`/weight/data?range=${range}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                loader.textContent = "Failed to load data.";
                return;
            }

            // Replace 'T' with a space in date labels
            const labels = data.map(record => record.date.replace('T', ' '));
            const values = data.map(record => record.weight);

            // Render the chart
            const ctx = chartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Weight (kg)',
                        data: values,
                        borderColor: 'hsl(183, 44%, 41%)',
                        backgroundColor: 'hsla(183, 44%, 41%, 0.2)',
                        borderWidth: 2,
                        tension: 0.4,
                    }]
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
                                    return `${context.parsed.y} kg`;
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
                                text: 'Weight (kg)'
                            }
                        }
                    }
                }
            });

            // Hide loader and show chart
            loader.classList.add("d-none");
            chartCanvas.classList.remove("d-none");
        })
        .catch(error => {
            console.error('Error fetching weight data:', error);
            loader.textContent = "Failed to load data.";
        });
});
