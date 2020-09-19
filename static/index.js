// showChat();

// Tombol Chat
$('#prime').click(function () {
    toggleFab();
});

// Ubah bentuk tombol chat
function toggleFab() {
    $('.prime').toggleClass('zmdi-comments');
    $('.prime').toggleClass('zmdi-close');
    $('.prime').toggleClass('is-active');
    $('.prime').toggleClass('is-visible');
    $('#prime').toggleClass('is-float');
    $('.chat').toggleClass('is-visible');
    $('.fab').toggleClass('is-visible');

}

// Connext to socker
var socket = io();
socket.on("connect", function () {
    socket.emit("send message", {
        message: "I'm connected!"
    }); // message yg user input
    socket.on("response message", (data) => {
        console.log(data);
    }); // listen event from server
});