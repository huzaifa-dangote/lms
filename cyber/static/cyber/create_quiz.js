document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('create-quiz-button').style.display = 'none';

});

function expand_nav() {
    var x = document.getElementById("collapsed-nav");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

// Declare counter for creating quiz questions
let questionCount = 0;

function addQuestion() {
    if (questionCount >= 10) return;

    const container = document.getElementById('questions-container');
    const questionDiv = document.createElement('div');

    questionDiv.innerHTML = `
        <p>
            Question ${questionCount + 1}
        </p>
        <textarea style="width:70%" class="w3-input w3-border w3-round" name="question_${questionCount}" rows="4" placeholder="Type question"></textarea>
        <div>
            ${[0, 1, 2, 3].map(j => `
                <div>
                    <input class="choice-input" type="text" name="choice_${questionCount}_${j}" placeholder="Choice ${j + 1}">
                    <input type="checkbox" name="is_correct_${questionCount}_${j}">
                </div>
            `).join('')}
        </div>
    `;
    container.appendChild(questionDiv);
    questionCount++;

    if (questionCount === 10) {
        document.getElementById('add-question-button').style.display = 'none';
        document.getElementById('create-quiz-button').style.display = 'block';
    }
}