document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("chartLoader");
    const chartCanvas = document.getElementById("medicationsChart");

    // Extract the selected range from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const range = urlParams.get('range') || 'last_week'; // Default to 'last_week'

    // Fetch medication data with the selected range
    fetch(`/medications/data?range=${range}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                loader.innerHTML = "<span class='text-danger'>No data available for the selected range.</span>";
                throw new Error("No data received or invalid format");
            }

            // Group data by date
            const groupedData = data.reduce((acc, record) => {
                const dateKey = new Date(record.date).toISOString().split("T")[0]; // Extract only the date part
                if (!acc[dateKey]) {
                    acc[dateKey] = { taken: 0, missed: 0 };
                }
                if (record.status === "Taken") {
                    acc[dateKey].taken++;
                } else {
                    acc[dateKey].missed++;
                }
                return acc;
            }, {});

            // Prepare labels and datasets for the chart
            const labels = Object.keys(groupedData);
            const takenData = labels.map(date => groupedData[date].taken);
            const missedData = labels.map(date => groupedData[date].missed);

            const chartData = {
                labels: labels,
                datasets: [
                    {
                        label: "Taken",
                        backgroundColor: "hsl(120, 100%, 25%)",
                        data: takenData
                    },
                    {
                        label: "Missed",
                        backgroundColor: "hsl(0, 100%, 50%)",
                        data: missedData
                    }
                ]
            };

            // Render the bar chart
            const ctx = chartCanvas.getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "top",
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `${context.dataset.label}: ${context.raw}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Date"
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Number of Medications"
                            },
                            beginAtZero: true
                        }
                    }
                }
            });

            // Hide loader and show chart
            loader.classList.add("d-none");
            chartCanvas.classList.remove("d-none");
        })
        .catch(error => {
            console.error("Error fetching or processing medication data:", error);
        });
});
