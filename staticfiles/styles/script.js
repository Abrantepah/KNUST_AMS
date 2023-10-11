// static/styles/script.js

document.addEventListener('DOMContentLoaded', function () {
  const countdownElement = document.getElementById('countdown');
  const initialTimeRemaining = parseInt(countdownElement.textContent);

  function updateCountdown() {
    let timeRemaining = parseInt(countdownElement.textContent);

    const interval = setInterval(() => {
      if (timeRemaining <= 0) {
        countdownElement.textContent = 'Time expired';
        clearInterval(interval);
        // Optionally, you can perform actions when the time expires
      } else {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        countdownElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        timeRemaining--;
      }
    }, 1000);
  }

  updateCountdown();
});

// ################ mark button operation ###############
function markAttendance() {
    var button = document.getElementById("mark-attendance");
    button.classList.add("clicked");
    button.innerHTML = "Marked Present";
    button.disabled = true;
  }



// Function to filter students based on the select and input values
function filterStudents() {
  const indexFilterValue = document.getElementById('indexFilter').value;
  const courseFilterValue = document.getElementById('courseFilter').value;
  const yearFilterValue = document.getElementById('yearFilter').value;
  const strikesFilterValue = document.getElementById('strikesFilter').value;
  const nameFilterValue = document.getElementById('nameFilter').value.toLowerCase();

  const filteredStudents = students.filter((student) => {
    return (
      (indexFilterValue === '' || student.index === indexFilterValue) &&
      (courseFilterValue === '' || student.course === courseFilterValue) &&
      (yearFilterValue === '' || student.year === yearFilterValue) &&
      (strikesFilterValue === '' || student.strikes.toString() === strikesFilterValue) &&
      student.name.toLowerCase().includes(nameFilterValue)
    );
  });

  renderStudents(filteredStudents);
}

// Function to render the filtered student rows in the table
function renderStudents(filteredStudents) {
  const tableBody = document.querySelector('#studentsTable tbody');
  tableBody.innerHTML = '';

  filteredStudents.forEach((student) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${student.index}</td>
      <td>${student.course}</td>
      <td>${student.year}</td>
      <td>${student.strikes}</td>
      <td>${student.name}</td>
    `;

    tableBody.appendChild(row);
  });
}

// Add event listener to the filter button
document.getElementById('filterButton').addEventListener('click', filterStudents);

// ########## active reports sidenav ########
function showContent(url, link) {
  // Remove active class from all links
  var links = document.querySelectorAll('.sidebar a');
  links.forEach(function(link) {
    link.classList.remove('active');
  });

  // Set active class to the clicked link
  link.classList.add('active');

  // Your code to load and display the content
  // ...
  fetch(url)
  .then(response => response.text())
  .then(content => {
    document.getElementById("content-placeholder").innerHTML = content;
  })
  .catch(error => console.log(error));
}



//#######toggle button#####

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const toggleButton = document.querySelector('.toggle-button');
  
  sidebar.classList.toggle('collapsed');
  
  if (sidebar.classList.contains('collapsed')) {
    toggleButton.style.left = '20px';
  } else {
    toggleButton.style.left = '150px';
    toggleButton.style.borde='2px solid rgb(31, 31, 31)';
  }
}



//##### accept and decline button functionality 

function handleAccept(button) {
  const tr = button.closest('tr');

  tr.querySelector('.accept-button').classList.add('Adeeper');
  tr.querySelector('.accept-button').textContent = 'Accepted';
  tr.querySelector('.decline-button').classList.add('hide');
  tr.querySelector('.accept-button').disabled = true;
  tr.querySelector('.decline-button').disabled = true;
  tr.querySelector('.view-file-button').disabled = true;
  tr.querySelector('.view-file-button').textContent = 'Viewed';
}

function handleDecline(button) {
  const tr = button.closest('tr');

  tr.querySelector('.decline-button').classList.add('Ddeeper');
  tr.querySelector('.decline-button').textContent = 'Declined';
  tr.querySelector('.accept-button').classList.add('hide');
  tr.querySelector('.accept-button').disabled = true;
  tr.querySelector('.decline-button').disabled = true;
  tr.querySelector('.view-file-button').disabled = true;
  tr.querySelector('.view-file-button').textContent = 'Viewed';
}

function viewFile(button) {
  const tr = button.closest('tr');

  // Fetch the file content
  fetch('simpleFile')
    .then(response => response.text())
    .then(content => {
      // Display the prompt and get user input
      const userInput = prompt('File Content:\n\n' + content + '\n\nDo you accept?', 'Accept');

      // Process user input
      if (userInput && userInput.toLowerCase() === 'accept') {
        // User accepted
        alert('You accepted the file content.');
        // Do something else with the accepted content
        handleAccept(button);
      } else {
        // User declined or canceled
        alert('You declined the file content.');
        // Do something else or exit
        handleDecline(button);
      }

      button.textContent = 'Viewed';
      button.disabled = true;
    })
    .catch(error => {
      console.log('Error:', error);
    });
}


//####### Strike content color operation ###########

  // Get all the rows with class "strike-content"
  const strikeRows = document.querySelectorAll('.strike-content');

  // Loop through each row
  strikeRows.forEach(row => {
    // Get the strike content value
    const strikeContent = parseInt(row.textContent);

    // Determine the appropriate class based on the strike content value
    let rowClass = '';
    if (strikeContent === 1) {
      rowClass = 'table-success';
    } else if (strikeContent === 2) {
      rowClass = 'table-warning';
    } else if (strikeContent === 3) {
      rowClass = 'table-danger';
    }

    // Add the class to the row
    row.closest('tr').classList.add(rowClass);
  });

// ##############help##########
function generateAnswer(faqNumber) {
  const answerContainer = document.createElement('div');
  answerContainer.classList.add('message');

  const sender = document.createElement('div');
  sender.classList.add('message-sender');
  sender.textContent = 'Bot';
  answerContainer.appendChild(sender);

  const answer = document.createElement('div');
  answer.classList.add('message-content');

  switch (faqNumber) {
    case 1:
      answer.textContent = 'To create an account, click on the "Sign Up" button and fill out the registration form.';
      break;
    case 2:
      answer.textContent = 'We accept various payment methods including credit cards, PayPal, and bank transfers.';
      break;
    case 3:
      answer.textContent = 'You can track your order by logging into your account and navigating to the "Order History" section.';
      break;
    default:
      answer.textContent = 'Sorry, I don\'t have an answer for that question.';
  }

  answerContainer.appendChild(answer);
  document.querySelector('.chat-messages').appendChild(answerContainer);
}


