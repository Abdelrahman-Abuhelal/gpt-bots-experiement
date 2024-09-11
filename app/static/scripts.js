$(document).ready(function () {
  $('#send-button').click(function () {
    sendMessage();
  });

  $('#message-input').keypress(function (event) {
    if (event.which === 13) { // Enter key pressed
      event.preventDefault(); // Prevent form submission
      sendMessage();
    }
  });

  function sendMessage() {
    const message = $('#message-input').val().trim();
    if (message === '') {
      return; 
    }

    appendMessage(message, 'user');

    $.ajax({
      url: '/api',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ message: message }),
      success: function (response) {
        appendMessage(response, 'response');
      },
      error: function () {
        appendMessage('Error: Failed to send the message.', 'response');
      }
    });

    $('#message-input').val('');
  }

  function appendMessage(text, type) {
    const messageHtml = `
      <div class="message ${type}">
        <div class="message-content">${text}</div>
      </div>
    `;

    $('#chat-container').append(messageHtml);
    $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
  }
});
