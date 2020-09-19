const submitButton = document.getElementById("fab_send");
const chatbotInput = document.getElementById("chatSend");

submitButton.onclick = userSubmitEventHandler;
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