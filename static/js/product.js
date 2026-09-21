document.addEventListener('DOMContentLoaded', () => {

    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const table = document.getElementById('productTable');
    const tbody = table ? table.querySelector('tbody') : null;
    const resultCount = document.getElementById('resultCount');
    const rows = tbody ? Array.from(tbody.querySelectorAll('tr[data-name]')) : [];

    function applyFilters() {
        const keyword = searchInput ? searchInput.value.trim().toLowerCase() : '';
        const category = categoryFilter ? categoryFilter.value : 'all';
        let visibleCount = 0;

        rows.forEach((row) => {
            const matchName = row.dataset.name.includes(keyword);
            const matchCategory = category === 'all' || row.dataset.category === category;
            const visible = matchName && matchCategory;

            row.classList.toggle('row-hidden', !visible);
            if (visible) visibleCount++;
        });

        if (resultCount) {
            resultCount.textContent = rows.length
                ? `Menampilkan ${visibleCount} dari ${rows.length} produk`
                : '';
        }
    }

    if (searchInput) searchInput.addEventListener('input', applyFilters);
    if (categoryFilter) categoryFilter.addEventListener('change', applyFilters);

    applyFilters();

    const sortState = {};

    table.querySelectorAll('th[data-sort]').forEach((th) => {
        th.addEventListener('click', () => {
            const key = th.dataset.sort;
            const asc = !sortState[key];
            sortState[key] = asc;

            const sorted = [...rows].sort((a, b) => {
                let valA, valB;

                if (key === 'index') {
                    valA = rows.indexOf(a);
                    valB = rows.indexOf(b);
                } else if (key === 'price' || key === 'stock') {
                    valA = parseFloat(a.dataset[key]);
                    valB = parseFloat(b.dataset[key]);
                } else {
                    valA = a.dataset[key];
                    valB = b.dataset[key];
                }

                if (valA < valB) return asc ? -1 : 1;
                if (valA > valB) return asc ? 1 : -1;
                return 0;
            });

            sorted.forEach((row) => tbody.appendChild(row));
        });
    });

    const deleteModal = document.getElementById('deleteModal');
    const deleteProductName = document.getElementById('deleteProductName');
    const cancelDelete = document.getElementById('cancelDelete');
    const confirmDelete = document.getElementById('confirmDelete');
    let formToSubmit = null;

    document.querySelectorAll('.delete-form').forEach((form) => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            formToSubmit = form;
            deleteProductName.textContent = form.dataset.productName || 'produk ini';
            deleteModal.classList.add('show');
        });
    });

    function closeModal() {
        deleteModal.classList.remove('show');
        formToSubmit = null;
    }

    if (cancelDelete) cancelDelete.addEventListener('click', closeModal);

    if (deleteModal) {
        deleteModal.addEventListener('click', (e) => {
            if (e.target === deleteModal) closeModal();
        });
    }

    if (confirmDelete) {
        confirmDelete.addEventListener('click', () => {
            if (formToSubmit) formToSubmit.submit();
        });
    }
});