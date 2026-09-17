const deleteForms = document.querySelectorAll(".delete-form");

deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
        const confirmed = confirm(
            "Yakin ingin menghapus produk ini?"
        );

        if (!confirmed) {
            event.preventDefault();
        }
    });
});

const searchInput =
    document.getElementById("searchInput");

const categoryFilter =
    document.getElementById("categoryFilter");


function filterProducts() {

    const searchValue =
        searchInput.value.toLowerCase();

    const categoryValue =
        categoryFilter.value;


    const rows =
        document.querySelectorAll(
            "#productTable tbody tr"
        );


    rows.forEach(function (row) {

        const name =
            row.children[1]?.textContent
                .toLowerCase();

        const category =
            row.children[2]?.textContent
                .trim();


        const matchName =
            name?.includes(searchValue);

        const matchCategory =
            categoryValue === "all" ||
            category === categoryValue;


        if (matchName && matchCategory) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });
}


if (searchInput) {

    searchInput.addEventListener(
        "input",
        filterProducts
    );

}


if (categoryFilter) {

    categoryFilter.addEventListener(
        "change",
        filterProducts
    );

}

document.addEventListener("DOMContentLoaded", function () {

    const salesChart = document.getElementById("salesChart");

    if (salesChart && window.salesChartData) {

        const labels = window.salesChartData.map(
            item => item.date
        );

        const revenues = window.salesChartData.map(
            item => item.revenue
        );

        new Chart(salesChart, {
            type: "line",

            data: {
                labels: labels,

                datasets: [
                    {
                        label: "Omzet",
                        data: revenues,

                        tension: 0.4,

                        fill: true
                    }
                ]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    },

                    tooltip: {
                        callbacks: {
                            label: function(context) {

                                const value = context.parsed.y;

                                return "Omzet: Rp " +
                                    value.toLocaleString("id-ID");
                            }
                        }
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,

                        ticks: {
                            callback: function(value) {

                                return "Rp " +
                                    value.toLocaleString("id-ID");
                            }
                        }
                    }
                }
            }
        });
    }

});