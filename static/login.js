function getAccountType() {
    return document.querySelector('input[name="accountType"]:checked').value;
}

function createAccount() {
    const name = document.getElementById("name").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const accountType = getAccountType();

    const endpoint =
        accountType === "business"
            ? "/api/login/create-business"
            : "/api/login/create-customer";

    fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, username, password })
    })
        .then((res) => res.json())
        .then((data) => {
            const status = document.getElementById("status");
            if (data.success) {
                status.innerText = "Account created! Please log in.";
            } else {
                status.innerText = "Error: " + (data.error || "Account creation failed.");
            }
        });
}

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const accountType = getAccountType();

    const endpoint =
        accountType === "business"
            ? "/api/login/business"
            : "/api/login/customer";

    fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
        .then((res) => res.json())
        .then((data) => {
            const status = document.getElementById("status");
            if (data.success) {
                const id = data.user_id || data.account_id;
                localStorage.setItem("accountType", accountType);
                localStorage.setItem("accountId", id);
                status.innerText = "Login successful!";
                // Redirect logic here
                window.location.href = accountType === "business" ? "/manage" : "/search";
            } else {
                status.innerText = "Error: " + (data.error || "Login failed.");
            }
        });
}
