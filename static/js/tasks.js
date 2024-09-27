document.addEventListener('DOMContentLoaded', function() {
    const addTaskForm = document.getElementById('addTaskForm');
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', addTask);
    }

    const taskList = document.getElementById('taskList');
    if (taskList) {
        taskList.addEventListener('change', updateTaskStatus);
    }
});

function addTask(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/add_task', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            location.reload();
        } else {
            showNotification('Error adding task', 'error');
        }
    });
}

function updateTaskStatus(event) {
    if (event.target.tagName === 'SELECT') {
        const taskId = event.target.dataset.taskId;
        const newStatus = event.target.value;

        fetch(`/update_task_status/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrf_token')
            },
            body: `status=${newStatus}`
        }).then(response => {
            if (response.ok) {
                showNotification('Task status updated', 'info');
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
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrf_token')
            }
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                showNotification('Error deleting task', 'error');
            }
        });
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
