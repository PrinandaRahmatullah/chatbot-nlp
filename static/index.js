// showChat();

// Tombol Chat
$("#prime").click(function () {
	toggleFab();
});

// Ubah bentuk tombol chat
function toggleFab() {
	$(".prime").toggleClass("zmdi-comments");
	$(".prime").toggleClass("zmdi-close");
	$(".prime").toggleClass("is-active");
	$(".prime").toggleClass("is-visible");
	$("#prime").toggleClass("is-float");
	$(".chat").toggleClass("is-visible");
	$(".fab").toggleClass("is-visible");
}

// Connext to socket
var socket = io();
socket.on("connect", function () {
	var sendButton = $("#fab_send");
	var chatbotInput = $("#chatSend");

	// if ($.trim(chatbotInput.val()) != "") {}
	chatbotInput.keypress(function (event) {
		var keycode = event.which;
		if (keycode == 13) {
			sendButton.click();
		}
	});

	sendButton.click(function () {
		// message yg user input
		socket.emit("send message", chatbotInput.val());

		$("div#chat_fullscreen").append(
			'<span class="chat_msg_item chat_msg_item_user">' +
			chatbotInput.val() +
			"</span>"
		);
		chatbotInput.val("");
	});

	// listen event from server
	socket.on("response message", (data) => {
		// console.log(data);
		$("div#chat_fullscreen").append(
			"<span class='chat_msg_item chat_msg_item_admin'><div class='chat_avatar'><img src='../assets/chatbots-logo.png'/></div>" +
			data +
			"</span>"
		);

		// Auto scroll to last element
		const chat_container = document.querySelector('#chat_fullscreen')
		chat_container.scrollTop = chat_container.lastChild.offsetTop - 10
	});
});