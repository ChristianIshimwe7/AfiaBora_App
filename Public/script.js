// Dummy health data and user credentials
const healthData = {
    heartRate: "75 bpm",
    calories: "2,300 kcal",
    weight: "68 kg"
  };
  
  const users = [
    { email: "test@example.com", password: "12345" }
  ];
  
  // Handle login
  function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    const user = users.find(u => u.email === email && u.password === password);
  
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
      alert("Login successful!");
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid email or password.");
    }
  }
  
  // Display health data
  function displayDashboard() {
    if (!localStorage.getItem("user")) {
      alert("Please log in first.");
      window.location.href = "login.html";
    }
  
    document.getElementById("heart-rate").textContent = `Heart Rate: ${healthData.heartRate}`;
    document.getElementById("calories").textContent = `Calories: ${healthData.calories}`;
    document.getElementById("weight").textContent = `Weight: ${healthData.weight}`;
  }
  
  // Logout function
  function handleLogout() {
    localStorage.removeItem("user");
    alert("Logged out successfully.");
    window.location.href = "login.html";
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("login-form")) {
      document.getElementById("login-form").addEventListener("submit", handleLogin);
    }
  
    if (document.getElementById("logout-btn")) {
      document.getElementById("logout-btn").addEventListener("click", handleLogout);
    }
  
    if (document.getElementById("dashboard-content")) {
      displayDashboard();
    }
  });
  