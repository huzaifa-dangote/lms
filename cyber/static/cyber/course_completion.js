function expand_nav() {
    var x = document.getElementById("collapsed-nav");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const userId = document.querySelector('#user-id').innerHTML;
    const courseId = document.querySelector('#course-id').innerHTML;

    // Check if user is at the bottom of the page
    window.onscroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            fetch(`/course_completion/${courseId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    completed_by: userId
                })
            })
        }
    }
})