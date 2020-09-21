const sendButton = document.getElementById("fab_send");
const chatbotInput = document.getElementById("chatSend");

sendButton.onclick = userSubmitEventHandler;
chatbotInput.onkeyup = userSubmitEventHandler;

function userSubmitEventHandler(event) {
    if (
        (event.keyCode && event.keyCode === 13) ||
        event.type === 'click'
    ) {
        // chatbotOutput.innerText = 'thinking...';
        console.log(chatbotInput.value);
    }
}