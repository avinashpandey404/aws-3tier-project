const API_URL = "http://51.20.253.244:5000";

// GET HTML ELEMENTS
const userForm = document.getElementById("userForm");
const userList = document.getElementById("userList");

// -----------------------------------
// FETCH USERS FROM BACKEND
// -----------------------------------
async function fetchUsers() {

    const response = await fetch(`${API_URL}/users`);

    const users = await response.json();

    userList.innerHTML = "";

    users.forEach(user => {

        const li = document.createElement("li");

        li.textContent = `${user.name} - ${user.email}`;

        userList.appendChild(li);
    });
}

// -----------------------------------
// ADD USER
// -----------------------------------
userForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    await fetch(`${API_URL}/users`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name,
            email: email
        })

    });

    // CLEAR FORM
    userForm.reset();

    // REFRESH USERS
    fetchUsers();
});

// LOAD USERS WHEN PAGE LOADS
fetchUsers();
