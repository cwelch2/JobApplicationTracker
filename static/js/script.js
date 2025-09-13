
// ---------- Search bar ------------
function filterJobs() {
    const input = document.getElementById("search-bar").value.toLowerCase();
    const rows = document.querySelectorAll(".job-row");

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(input) ? "" : "none";
    });
}

// ---------- Options menu ------------
function toggleOptionsMenu(event, jobId) {
    event.stopPropagation();
    document.querySelectorAll('.options-menu').forEach(m => m.classList.remove('open'));
    const menu = document.querySelector(`[data-menu-id="${jobId}"]`);
    menu.classList.toggle('open');
}

// Close menu when clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.options-menu').forEach(m => m.classList.remove('open'));
});



// ---------- Edit modal functions ------------
function openEditModal(id, title, company, location, status, link) {
    document.getElementById('edit-job-id').value = id;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-company').value = company;
    document.getElementById('edit-location').value = location;
    document.getElementById('edit-link').value = link || '';
    document.getElementById('edit-status').value = status;

    // Set form action
    const editForm = document.getElementById('editForm');
    editForm.action = `/update/${id}`;

    // Display modal
    document.getElementById('editModal').style.display = 'flex';

    // Close any open options menu
    document.querySelectorAll('.options-menu').forEach(m => m.classList.remove('open'));
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}



// ---------- Delete modal functions ------------
function openDeleteModal(id) {
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/delete/${id}`;

    document.getElementById('deleteModal').style.display = 'flex';

    // Close any open options menu
    document.querySelectorAll('.options-menu').forEach(m => m.classList.remove('open'));
}

function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}



// ---------- Add modal functions ------------
function openAddJobModal() {
    document.getElementById('addJobModal').style.display = 'flex';
}

function closeAddJobModal() {
    document.getElementById('addJobModal').style.display = 'none';
}



// Close modal on outside click
window.onclick = function (event) {
    const editModal = document.getElementById('editModal');
    const deleteModal = document.getElementById('deleteModal');
    const addModal = document.getElementById('addJobModal');

    if (event.target === editModal) {
        closeEditModal();
    }
    if (event.target === deleteModal) {
        closeDeleteModal();
    }
    if (event.target === addJobModal) {
        closeAddJobModal();
    }
};
