document.addEventListener('DOMContentLoaded', function () {

    search_quizzes();
});

function expand_nav() {
    var x = document.getElementById("collapsed-nav");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

function search_quizzes() {
    const searchInput = document.getElementById('search-input');
    const resultsDiv = document.getElementById('results');

    const fetchResults = () => {
        const quizTitle = searchInput.value;
        const userId = document.getElementById('user-id').innerHTML;

        fetch(`/quiz_search_result/${userId}?quiz_title=${quizTitle}`)
            .then(response => response.text())
            .then(data => {
                console.log(data);
                resultsDiv.innerHTML = data;
            });
    };

    searchInput.addEventListener('input', fetchResults);
}