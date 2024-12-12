function expand_nav() {
    var x = document.getElementById("collapsed-nav");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

function load_inbox() {
    document.querySelector('#inbox-container').style.display = 'block';
    document.querySelector('#email-container').style.display = 'none';
}

function load_email(emailId) {
    document.querySelector('#inbox-container').style.display = 'none';
    document.querySelector('#email-container').style.display = 'block';

    const emailContainer = document.querySelector('#email-container');
    const userId = document.querySelector('#user-id').innerHTML;

    fetch(`/email/${emailId}`)
    .then(response => response.json())
    .then(email => {
        console.log(email);

        emailContainer.innerHTML = `
            <div style="cursor:pointer"><i onclick="load_inbox()" class="fa fa-arrow-left" style="font-size:20px"></i></div>
            <div>From: ${email.sender}</div>
            <div>To: ${email.recipients}</div>
            <div>Subject: ${email.subject}</div>
            <hr>
            <div id="email-content">${email.body}</div>
        `

        // Checks if phishing link is clicked
        const text = document.querySelector('#email-content').innerHTML;
        const regex = /https:\/\/.*?\.com/g;
        const newText = text.replace(regex, (match) => `<span class="clickable-link">${match}</span>`);
        document.querySelector('#email-content').innerHTML = newText;

        document.querySelectorAll('.clickable-link').forEach(span => {
            span.addEventListener('click', () => {

                // PUT request to indicate link was clicked
                fetch(`/email/${emailId}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        clicked_by: userId
                    })
                })

                // Load you_were_phished page
                window.location.href = `http://127.0.0.1:8000/you_were_phished`;

            });
        });
    })

}