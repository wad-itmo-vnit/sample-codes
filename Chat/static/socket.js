const socket = io();

socket.on('connect', () => {
    console.log('Connected!');
})

socket.on('message', (data) => {
    addChat(data.user, data.message);
})

form.onsubmit = (e) => {
    e.preventDefault();
    data = new FormData(form);
    if (data.get('message') && data.get('user')) {
        document.querySelector('#message').value = '';
        addChat(data.get('user'), data.get('message'));
        obj = {
            user: data.get('user'),
            message: data.get('message')
        }
    
        socket.emit('message', obj)
    }
}