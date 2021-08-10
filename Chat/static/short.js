const worker = new XMLHttpRequest();

worker.onreadystatechange = () => {
    if (worker.readyState == 4 && worker.status == 200) {
        resp = JSON.parse(worker.responseText)
        addChat(resp.user, resp.message)
    }
}

function shortPolling() {
    worker.open('POST', '/short/chat');
    worker.send()
}

setInterval(shortPolling, 1000);