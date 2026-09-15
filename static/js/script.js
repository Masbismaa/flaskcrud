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