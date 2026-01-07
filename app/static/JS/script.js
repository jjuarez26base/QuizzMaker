const menuButton = document.querySelector('.menuButton');
const sidebar = document.querySelector('aside');
const menuicon = document.querySelector('.menuIcon');
const addQuestion = document.getElementById('AddQuestion');

const toggleSidebar = () => {
  sidebar.classList.toggle('hidden');
  menuicon.classList.toggle('rotated');
}

function ToEditQuizPage() {
  console.log('This function does nothing right now.')
};

function addQuestionFunction() {
    // 1. Select the div to clone (give your original div an ID or class for easy selection)
    const original = document.querySelector('.quiz_maker_question');
    
    // 2. Clone the div and all its children (true = deep clone)
    const clone = original.cloneNode(true);

    // 3. Calculate the next question number
    const newQuestionNumber = document.querySelectorAll('.quiz_maker_question').length + 1;

    // 4. Update the Header text
    clone.querySelector('h3').innerText = `Question ${newQuestionNumber}`;

    // 5. Update IDs and Names for all inputs to keep them unique
    clone.querySelectorAll('input').forEach(input => {
        // Replace the "1" in names/ids with the new count (e.g., question_1 -> question_2)
        const oldId = input.id;
        const newId = oldId.replace(/_1|_1$/g, `_${newQuestionNumber}`);
        
        input.id = newId;
        input.name = newId;
        
        // Clear the values so the new question starts empty
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
  console.log('This element does not exist in this webpage.')
}
