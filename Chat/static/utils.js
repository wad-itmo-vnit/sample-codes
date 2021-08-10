const dialog = document.querySelector("#dialog");
const form = document.querySelector("#user-chat");
const http = new XMLHttpRequest();

function addChat(user, message) {
    mess = `<p><b>${user} :</b>${message}</p>`
    dialog.innerHTML += mess
}

http.onreadystatechange = () => {
    if (http.readyState == 4 && http.status == 200) {
        resp = JSON.parse(http.responseText)
        addChat(resp.user, resp.message);
    }
}

form.onsubmit = (e) => {
    e.preventDefault();
    data = new FormData(form);
    if (data.get('message') && data.get('user')) {
        document.querySelector('#message').value = '';
        addChat(data.get('user'), data.get('message'));
        http.open('POST', '/chat');
        http.send(data);
    }
}