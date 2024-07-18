const socket = io();

// Join the code block when the page loads
socket.emit('join_code_block', '{{ title }}');

// Listen for code updates
socket.on('code_update', function(updatedCode) {
    const codeElement = document.getElementById('code');
    codeElement.textContent = updatedCode;
    hljs.highlightElement(codeElement); // Reapply syntax highlighting
});

// Listen for mentor assignment
socket.on('mentor_assigned', function() {
    console.log('You are the mentor for this code block.');
});

// Update code on input change
const codeElement = document.getElementById('code');
codeElement.addEventListener('input', function() {
    socket.emit('update_code', codeElement.textContent); // Emit the updated code
});