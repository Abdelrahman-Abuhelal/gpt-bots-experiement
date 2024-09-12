  $(document).ready(function () {
    const userLogo = "{{ url_for('static', filename='images/user.png') }}";
    const systemLogo = "{{ url_for('static', filename='images/gpt.jpg') }}";
    
    $('#send-button').click(function () {
      sendMessage();
    });

    $('#message-input').keypress(function (event) {
      if (event.which === 13) {
        event.preventDefault();
        sendMessage();
      }
    });

    function sendMessage() {
      const message = $('#message-input').val().trim();
      if (message === '') {
        return;
      }

      appendMessage(message, 'user', userLogo);

      $.ajax({
        url: '/api',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: message }),
        success: function (response) {
          appendMessage(response, 'response', systemLogo);
        },
        error: function () {
          appendMessage('Error: Failed to send the message.', 'response', systemLogo);
        }
      });

      $('#message-input').val('');
    }

    function appendMessage(text, type, logo) {
      const messageHtml = `
        <div class="message ${type}">
          <img src="${logo}" alt="${type} logo" class="logo">
          <div class="message-content">${text}</div>
        </div>
      `;

      $('#chat-container').append(messageHtml);
      $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
    }
  });
