document.addEventListener('DOMContentLoaded', () => {
    const defaultModuleId = '1'; // Set the default module ID
    loadTasks(defaultModuleId);

    // Add event listeners to module links
    document.querySelectorAll('.module-link').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const moduleId = link.getAttribute('data-module-id');
            loadTasks(moduleId);
        });
    });

    function loadTasks(moduleId) {
        fetch(`/module/${moduleId}/tasks`)
            .then(response => response.json())
            .then(tasks => {
                const tasksContainer = document.getElementById('tasks-container');
                tasksContainer.innerHTML = ''; // Clear previous tasks

                for (const [taskId, task] of Object.entries(tasks)) {
                    const taskElement = document.createElement('a');
                    taskElement.href = `/module/${moduleId}/task/${taskId}`;
                    taskElement.textContent = task.title;
                    tasksContainer.appendChild(taskElement);

                    // Add a line break for each task
                    tasksContainer.appendChild(document.createElement('br'));
                }
            })
            .catch(error => {
                console.error('Error loading tasks:', error);
            });
    }
});
