Quizzma
Quizzma is a simplistic, dark-themed quiz management platform designed to help students study and prepare for school. By allowing users to create, edit, and take custom quizzes, Quizzma turns study material into an interactive experience.

🚀 Features
Unlimited Quiz Creation: Create as many quizzes as you need for any subject.

Full CRUD Functionality: Users can create, read, update, and delete their own quizzes.

Gamified Profiles: Each user has a profile tracking their Points and a customizable Bio.

Admin Management Dashboard:

Staff members can monitor site statistics.

Admins can delete any quiz on the platform.

Admins can activate or deactivate user accounts directly from the dashboard.

Mobile Responsive: A sidebar-driven navigation system designed for both desktop and mobile comfort.

🛠️ Tech Stack
Backend

Python / Django: The core logic and server-side framework.

Django Models: Used for structured data storage (Quizzes, Questions, Choices, Tags, and UserProfiles).

Frontend

HTML5 & CSS3: Custom styles featuring a dark-mode aesthetic for reduced eye strain.

JavaScript: Used for interactive UI elements like the sidebar and dynamic forms.

Design & Tools

VS Code: Primary development environment.

Canva & Coolers: Used for branding, logo design, and color palette selection.

Gemini & Copilot: Utilized for brainstorming and code optimization.

📊 Database Structure
The system is built on a relational database with the following key models:

UserProfile: Extends the default User model to include points, bios, and profile pictures.

Quizzes: Stores the quiz title, cover image, owner, and associated tags.

Questions & Choices: A one-to-many relationship allowing multiple questions per quiz and multiple choices per question.

Tags: Allows for categorization and easy searching of study materials.

🛣️ Project Milestones
1. Planning Phase

Brainstorming sessions to establish the "Quizzma" identity. We defined the basic layout, split backend and frontend responsibilities, and set our end goals for the user experience.

2. Design

Focused on a "simplistic" philosophy. We chose dark colors to ensure better comfort for students during long night-time study sessions.

3. Development

Backend: Focused on heavy lifting first (Models, Views, and Authentication).

Frontend: Team collaboration on individual HTML pages and modular CSS.

4. Testing

Conducted through rigorous manual testing. Bugs were identified and fixed immediately in an iterative cycle to ensure stability.

⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/quizzma.git
cd quizzma
Set up a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Django:

Bash
pip install django
Apply Migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Create an Admin Account:

Bash
python manage.py createsuperuser
Run the Server:

Bash
python manage.py runserver
Access the site at http://127.0.0.1:8000/

👥 Credits
Jason & Jesuse: Backend architecture and heavy lifting.

Angel: Backend support and logic.

Design & Frontend: Collaborative effort by the Quizzma team.

Created between Dec 29th, 2025 – Jan 12th, 2026.

