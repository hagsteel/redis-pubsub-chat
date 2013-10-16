var socket = io.connect('/chat');

socket.on('on_chat_message', function(chatMessage) {
    console.log(chatMessage);
    var $chatMessages = $(".chat-messages");
    var message = $("<li>");
    message.text(chatMessage.nickname + ' says ' + chatMessage.message);
    $(".chat-messages").prepend(message);
});

$(document).ready(function() {
    $("#send-chat-action").click(function() {
        emitChat();
    });

    $("#chat-message").keyup(function(e, k) {
        if (e.keyCode == 13) {
            emitChat();
        }
    });
});

function emitChat() {
    var message = $("#chat-message").val();
    var nickname = $("#chat-nickname").val();
    if (message.length > 0) {
        socket.emit("chat", nickname, message);
        $("#chat-message").val('');
    }
}