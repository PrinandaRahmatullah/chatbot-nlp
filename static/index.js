// Tombol Chat
document.querySelector("#prime").addEventListener("click", () => {
	toggleFab()
});

// Ubah bentuk tombol chat
function toggleFab() {
	document.querySelector(".prime").classList.toggle("zmdi-comments")
	document.querySelector(".prime").classList.toggle("zmdi-close")
	document.querySelector(".prime").classList.toggle("is-active")
	document.querySelector(".prime").classList.toggle("is-visible")
	document.querySelector("#prime").classList.toggle("is-float")
	document.querySelector(".chat").classList.toggle("is-visible")
	document.querySelector(".fab").classList.toggle("is-visible")
}

// Connext to socket
var socket = io();
socket.on("connect", function () {
	var sendButton = document.querySelector("#fab_send")
	var chatbotInput = document.querySelector("#chatSend")

	chatbotInput.addEventListener("keypress", (event) => {
		var keycode = event.which;
		if (keycode == 13) {
			chatbotInput.value = chatbotInput.value.replace(/^\s+/g, "")
			if (chatbotInput.value === "") {} else if (chatbotInput.value != null && chatbotInput.value != "") {
				sendButton.click()
			}
		}
	});

	sendButton.addEventListener("click", () => {
		// message yg user input
		chatbotInput.value = chatbotInput.value.replace(/^\s+/g, "")
		if (chatbotInput.value != null && chatbotInput.value != "") {
			socket.emit("send message", chatbotInput.value);

			document.querySelector("div#chat_fullscreen").insertAdjacentHTML("beforeend",
				'<span class="chat_msg_item chat_msg_item_user">' +
				chatbotInput.value +
				"</span>"
			);
			// console.log(chatbotInput.val())
			chatbotInput.value = null;
		}
	});

	// listen event from server
	socket.on("response message", (data) => {
		document.querySelector("div#chat_fullscreen").insertAdjacentHTML("beforeend",
			"<span class='chat_msg_item chat_msg_item_admin'><div class='chat_avatar'><img src='../assets/chatbots-logo.png'/></div>" +
			data + "</span>"
		);

		// Auto scroll to last element
		const chat_container = document.querySelector("#chat_fullscreen");
		chat_container.scrollTop = chat_container.lastChild.offsetTop - 10;
	});
});