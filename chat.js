document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    document.getElementById('message-form').onsubmit = function(e){
        e.preventDefault();
        let messageInput = document.getElementById('input');
        let roomInput = document.getElementById('room');
        if (messageInput.value && roomInput.value) {
            socket.emit('message', {message: messageInput.value, room: roomInput.value});
            messageInput.value = '';
        }
    };

    document.getElementById('file-form').onsubmit = function(e) {
        e.preventDefault();
        let fileInput = document.querySelector('input[type="file"]');
        let formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                alert('File uploaded successfully.');
            } else {
                alert('Upload failed.');
            }
        });
    };

    socket.on('message', function(data) {
        var item = document.createElement('li');
        item.textContent = data.message;
        document.getElementById('messages').appendChild(item);
        window.scrollTo(0, document.body.scrollHeight);
    });
});
