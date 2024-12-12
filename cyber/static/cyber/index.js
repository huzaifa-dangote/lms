document.addEventListener('DOMContentLoaded', function () {

    search_courses();
});

function expand_nav() {
  var x = document.getElementById("collapsed-nav");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else { 
    x.className = x.className.replace(" w3-show", "");
  }
}

function search_courses() {
    const searchInput = document.getElementById('search-input');
    const resultsDiv = document.getElementById('results');

    const fetchResults = () => {
        const courseTitle = searchInput.value;
        const userId = document.getElementById('user-id').innerHTML;

        fetch(`/course_search_result/${userId}?course_title=${courseTitle}`)
            .then(response => response.text())
            .then(data => {
                console.log(data);
                resultsDiv.innerHTML = data;
            });
    };

    searchInput.addEventListener('input', fetchResults);
}