const menuButton = document.querySelector('.menuButton');
const sidebar = document.querySelector('aside');
const menuicon = document.querySelector('.menuIcon');


const toggleSidebar = () => {
  sidebar.classList.toggle('hidden');
  menuicon.classList.toggle('rotated');
}

menuButton.addEventListener('click', toggleSidebar);

function ToEditQuizPage() {
    console.log('This function does nothing right now.')
  };