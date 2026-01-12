const menuButton = document.querySelector('.menuButton');
const sidebar = document.querySelector('aside');
const menuicon = document.querySelector('.menuIcon');
const addQuestion = document.getElementById('AddQuestion');
const cleanbtn = document.querySelector('.cleanbtn');
const hider = document.querySelector('.hiddenornot');

if (cleanbtn && hider) {
    cleanbtn.addEventListener('click', () => {
        hider.classList.toggle('hiddenornot');
    });
}

const toggleSidebar = () => {
    sidebar.classList.toggle('hidden');
    menuicon.classList.toggle('rotated');
};



async function deleteQuestion(questionId, deleteId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/delete_question/${deleteId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest'},
            mode: 'same-origin'
        });

        if (response.ok) {
            const question = document.getElementById(`question-${questionId}`);
            if (question) {
                question.remove();
                reIndexQuestions();
            }
        } else {
            alert("Error: Could not delete the question from the database.");
        }
    } catch (error) {
        console.error("Network error:", error);
    }
}

function reIndexQuestions() {
    const questions = document.querySelectorAll('.quiz_maker_question');

    questions.forEach((question, index) => {
        const newNumber = index + 1;
        const title = question.querySelector('h3');

        if (title) {
            title.textContent = `Question ${newNumber}`;
        }

        question.id = `question-${newNumber}`;

        const deleteBtn = question.querySelector('button');
        if (deleteBtn) {
            const currentOnClick = deleteBtn.getAttribute('onclick');
            const updatedOnClick = currentOnClick.replace(/'\d+'/, `'${newNumber}'`);
            deleteBtn.setAttribute('onclick', updatedOnClick);
        }

        const inputs = question.querySelectorAll('input');
        inputs.forEach(input => {
            const oldId = input.id;
            const newId = oldId.replace(/\d+/, newNumber);
            input.id = newId;
            input.name = newId;
        });
    });
}

function addQuestionFunction() {
    const original = document.querySelector('.quiz_maker_question');
    const clone = original.cloneNode(true);
    const newQuestionNumber = document.querySelectorAll('.quiz_maker_question').length + 1;

    clone.querySelector('h3').innerText = `Question ${newQuestionNumber}`;
    clone.querySelectorAll('input').forEach(input => {
        const oldId = input.id;
        const newId = oldId.replace(/_1|_1$/g, `_${newQuestionNumber}`);

        input.id = newId;
        input.name = newId;

        if (input.type === 'checkbox') {
            input.checked = false;
        } else {
            input.value = '';
        }

    document.getElementById('questionsContainer').appendChild(clone);
})};

menuButton.addEventListener('click', toggleSidebar);

try {
  addQuestion.addEventListener('click', addQuestionFunction);
} catch (error) {
}

// Show more / Show less for long bios
function attachBioToggle() {
    const bio = document.querySelector('.profile-bio');
    if (!bio) return;
    const btn = bio.querySelector('.bio-toggle');
    if (!btn) return;

    // Show toggle only if content overflows
    const isOverflowing = bio.scrollHeight > bio.clientHeight + 2; // small tolerance
    if (isOverflowing) {
        btn.style.display = 'inline-block';
    } else {
        btn.style.display = 'none';
        return;
    }

    // Remove previous handler if any to avoid double-binding
    btn.replaceWith(btn.cloneNode(true));
    const newBtn = bio.querySelector('.bio-toggle');

    newBtn.addEventListener('click', () => {
        const expanded = bio.classList.toggle('expanded');
        newBtn.textContent = expanded ? 'Show less' : 'Show more';
        newBtn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    });
}

// run on load and on resize so it reacts to layout changes
attachBioToggle();
window.addEventListener('resize', attachBioToggle);