document.addEventListener('DOMContentLoaded', function() {
    const addTaskForm = document.getElementById('addTaskForm');
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', addTask);
    }

    const taskTable = document.getElementById('taskTable');
    if (taskTable) {
        taskTable.addEventListener('change', updateTaskStatus);
    }
});

function addTask(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/add_task', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            location.reload();
        } else {
            showNotification('Error adding task', 'error');
        }
    });
}

function updateTaskStatus(event) {
    if (event.target.classList.contains('task-status')) {
        const taskId = event.target.dataset.taskId;
        const newStatus = event.target.value;

        fetch(`/update_task_status/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${newStatus}`
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
            } else {
                showNotification('Error updating task status', 'error');
            }
        });
    }
}

function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        fetch(`/delete_task/${taskId}`, {
            method: 'POST',
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                location.reload();
            } else {
                showNotification('Error deleting task', 'error');
            }
        });
    }
}
