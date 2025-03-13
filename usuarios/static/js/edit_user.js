document.addEventListener('DOMContentLoaded', function () {
    var editUserModal = document.getElementById('editUserModal');
    editUserModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var userId = button.getAttribute('data-id');
        var username = button.getAttribute('data-username');
        var role = button.getAttribute('data-role');

        var modalTitle = editUserModal.querySelector('.modal-title');
        var userIdInput = editUserModal.querySelector('#userId');
        var usernameInput = editUserModal.querySelector('#username');
        var roleInput = editUserModal.querySelector('#role');

        modalTitle.textContent = 'Modificar Usuario ' + username;
        userIdInput.value = userId;
        usernameInput.value = username;
        roleInput.value = role;

        document.getElementById('editUserForm').action = `/edit_user/${userId}/`;
    });
});
