const menuButton = document.querySelector('.menuButton');
const sidebar = document.querySelector('aside');
const menuicon = document.querySelector('.menuIcon');
const addQuestion = document.getElementById('AddQuestion');

const toggleSidebar = () => {
  sidebar.classList.toggle('hidden');
  menuicon.classList.toggle('rotated');
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
