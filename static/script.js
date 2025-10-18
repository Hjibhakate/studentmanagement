const form = document.getElementById('studentForm');
const tableBody = document.querySelector('#studentTable tbody');

window.onload = fetchStudents;

function fetchStudents() {
  fetch('/api/students')
    .then(res => res.json())
    .then(data => updateTable(data));
}

form.addEventListener('submit', function (e) {
  e.preventDefault();

  const name = document.getElementById('name').value.trim();
  const age = document.getElementById('age').value.trim();
  const grade = document.getElementById('grade').value.trim();

  if (name && age && grade) {
    fetch('/api/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, age, grade })
    })
    .then(() => {
      fetchStudents();
      form.reset();
    });
  }
});

function updateTable(students) {
  tableBody.innerHTML = '';

  students.forEach(student => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${student.name}</td>
      <td>${student.age}</td>
      <td>${student.grade}</td>
      <td><button class="delete-btn" onclick="deleteStudent('${student._id}')">Delete</button></td>
    `;
    tableBody.appendChild(row);
  });
}

function deleteStudent(id) {
  fetch(`/api/students/${id}`, {
    method: 'DELETE'
  }).then(() => fetchStudents());
}
