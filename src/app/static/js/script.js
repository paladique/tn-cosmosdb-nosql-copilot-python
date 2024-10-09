document.getElementById('message-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    const prompt = document.getElementById('prompt').value;  // Get the value from the textarea

    // Check if the prompt is not empty
    if (!prompt.trim()) {
        alert("Please enter a prompt");
        return;
    }

    try {
        const response = await fetch("{% url 'generate_response' session_id=session.session_id %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'  // Add the CSRF token for security
            },
            body: JSON.stringify({
                user_input: prompt  // Send prompt as part of JSON body
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Update the chat session with user's input
            const chatSession = document.getElementById('chat-session');
            chatSession.innerHTML += `
                <li class="message user">
                    <div class="content">
                        <p>${prompt}</p>
                    </div>
                </li>
                <li class="message assistant">
                    <div class="content">
                        <p>${data.response}</p>
                    </div>
                </li>
            `;

            // Scroll chat window to the bottom to show the new messages
            const chatWindow = document.querySelector('.chat-window');
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Clear the input field after submission
            document.getElementById('prompt').value = '';
        } else {
            console.error('Error:', data.error);
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Fetch Error:', error);
    }
});