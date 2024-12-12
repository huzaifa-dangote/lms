function expand_nav() {
    var x = document.getElementById("collapsed-nav");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const phishingLabels = JSON.parse(document.getElementById('phishing_labels-data').textContent);
    const courseLabels = JSON.parse(document.getElementById('course_labels-data').textContent);
    const quizLabels = JSON.parse(document.getElementById('quiz_labels-data').textContent);
    const phishingPieData = JSON.parse(document.getElementById('phishing-data').textContent);
    const coursePieData = JSON.parse(document.getElementById('course-data').textContent);
    const quizPieData = JSON.parse(document.getElementById('quiz-data').textContent);
    console.log(phishingLabels);
    console.log(phishingPieData);

    // Phishing Pie Chart
    new Chart('myPhishingPieChart', {
        type: 'doughnut',
        data: {
            labels: phishingLabels,
            datasets: [{
                data: phishingPieData,
                backgroundColor: ['#ff9999', '#99ff99'],
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Phishing'
            }, 
        }
    });

    // Course Pie Chart
    new Chart('myCoursePieChart', {
        type: 'doughnut',
        data: {
            labels: courseLabels,
            datasets: [{
                data: coursePieData,
                backgroundColor: ['#ff9999', '#99ff99'],
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Courses'
            }
        }
    });

    // Quiz Pie Chart
    new Chart('myQuizPieChart', {
        type: 'doughnut',
        data: {
            labels: quizLabels,
            datasets: [{
                data: quizPieData,
                backgroundColor: ['#ff9999', '#99ff99'],
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Quizzes'
            }
        }
    });
});