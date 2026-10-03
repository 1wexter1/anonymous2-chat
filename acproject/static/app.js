const socket = io();


const messages = document.getElementById("messages");

const form = document.getElementById("messageForm");

const input = document.getElementById("messageInput");

const status = document.getElementById("status");

const modal = document.getElementById("nameModal");

const nameInput = document.getElementById("nameInput");

const joinButton = document.getElementById("joinButton");


let myName = "";



/*
    Sunucuya bağlanınca
*/

socket.on("connect", () => {

    status.textContent = "Bağlı";

});



/*
    Sunucuyla bağlantı kesilirse
*/

socket.on("disconnect", () => {

    status.textContent = "Bağlantı kesildi";

});



/*
    Kullanıcı sohbete katılıyor
*/

joinButton.addEventListener("click", joinChat);



nameInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        joinChat();

    }

});



function joinChat() {

    myName = nameInput.value.trim();

    if (!myName) {

        myName = "Anonim";

    }

    myName = myName.substring(0, 24);


    socket.emit(
        "join",
        {
            name: myName
        }
    );


    modal.style.display = "none";

    input.focus();

}



/*
    Mesaj gönderme
*/

form.addEventListener("submit", (event) => {

    event.preventDefault();


    const text = input.value.trim();


    if (!text) {

        return;

    }


    if (!socket.connected) {

        return;

    }


    socket.emit(
        "message",
        {
            name: myName,
            text: text.substring(0, 1000)
        }
    );


    input.value = "";

    input.focus();

});



/*
    Yeni mesaj geldi
*/

socket.on("message", (data) => {

    addMessage(
        data.name,
        data.text
    );

});



/*
    Sistem mesajı
*/

socket.on("system_message", (data) => {

    addSystemMessage(data.text);

});



function addMessage(name, text) {

    const message = document.createElement("div");

    message.className = "message";


    const nameElement = document.createElement("strong");

    nameElement.textContent = name;


    const textElement = document.createElement("span");

    textElement.textContent = text;


    message.appendChild(nameElement);

    message.appendChild(textElement);


    messages.appendChild(message);


    messages.scrollTop = messages.scrollHeight;

}



function addSystemMessage(text) {

    const message = document.createElement("div");

    message.className = "system";


    message.textContent = text;


    messages.appendChild(message);


    messages.scrollTop = messages.scrollHeight;

}