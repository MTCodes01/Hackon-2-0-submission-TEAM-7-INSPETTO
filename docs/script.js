// Mock JSON data
const mockData = {
  users: {
    admin: "admin123",
    operator: "operator123",
    viewer: "viewer123",
  },
  cameras: [
    {
      id: "CAM001",
      location: "MG Road, Bangalore",
      coordinates: "12.9716, 77.5946",
      image: "placeholder.jpg",
      violations: 24,
    },
    {
      id: "CAM002",
      location: "Brigade Road, Bangalore",
      coordinates: "12.9698, 77.6085",
      image: "placeholder.jpg",
      violations: 18,
    },
    {
      id: "CAM003",
      location: "Residency Road, Bangalore",
      coordinates: "12.9719, 77.5937",
      image: "placeholder.jpg",
      violations: 31,
    },
    {
      id: "CAM004",
      location: "Commercial Street, Bangalore",
      coordinates: "12.9833, 77.6167",
      image: "placeholder.jpg",
      violations: 12,
    },
    {
      id: "CAM005",
      location: "Koramangala, Bangalore",
      coordinates: "12.9352, 77.6245",
      image: "placeholder.jpg",
      violations: 27,
    },
    {
      id: "CAM006",
      location: "Indiranagar, Bangalore",
      coordinates: "12.9784, 77.6408",
      image: "placeholder.jpg",
      violations: 15,
    },
    {
      id: "CAM001",
      location: "MG Road, Bangalore",
      coordinates: "12.9716, 77.5946",
      image: "placeholder.jpg",
      violations: 24,
    },
    {
      id: "CAM002",
      location: "Brigade Road, Bangalore",
      coordinates: "12.9698, 77.6085",
      image: "placeholder.jpg",
      violations: 18,
    },
    {
      id: "CAM003",
      location: "Residency Road, Bangalore",
      coordinates: "12.9719, 77.5937",
      image: "placeholder.jpg",
      violations: 31,
    },
    {
      id: "CAM004",
      location: "Commercial Street, Bangalore",
      coordinates: "12.9833, 77.6167",
      image: "placeholder.jpg",
      violations: 12,
    },
    {
      id: "CAM005",
      location: "Koramangala, Bangalore",
      coordinates: "12.9352, 77.6245",
      image: "placeholder.jpg",
      violations: 27,
    },
    {
      id: "CAM006",
      location: "Indiranagar, Bangalore",
      coordinates: "12.9784, 77.6408",
      image: "placeholder.jpg",
      violations: 15,
    },
  ],
  violations: {
    CAM001: [
      {
        id: 1,
        timestamp: "2025-07-12 14:30:00",
        beacon: "ABCDEF123456",
        plate: "KL 19 ABC",
        violations: 8,
      },
      {
        id: 2,
        timestamp: "2025-07-12 13:45:00",
        beacon: "GHIJKL789012",
        plate: "KA 05 XYZ",
        violations: 3,
      },
      {
        id: 3,
        timestamp: "2025-07-12 12:20:00",
        beacon: "MNOPQR345678",
        plate: "TN 32 DEF",
        violations: 12,
      },
      {
        id: 4,
        timestamp: "2025-07-12 11:15:00",
        beacon: "STUVWX901234",
        plate: "AP 28 GHI",
        violations: 5,
      },
      {
        id: 5,
        timestamp: "2025-07-12 10:30:00",
        beacon: "ABCDEF567890",
        plate: "KL 08 JKL",
        violations: 7,
      },
    ],
    CAM002: [
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
      {
        id: 2,
        timestamp: "2025-07-12 14:45:00",
        beacon: "HIJKLM890123",
        plate: "KL 19 ABC",
        violations: 4,
      },
      {
        id: 3,
        timestamp: "2025-07-12 13:30:00",
        beacon: "NOPQRS456789",
        plate: "TN 09 STU",
        violations: 9,
      },
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
      {
        id: 2,
        timestamp: "2025-07-12 14:45:00",
        beacon: "HIJKLM890123",
        plate: "KL 19 ABC",
        violations: 4,
      },
      {
        id: 3,
        timestamp: "2025-07-12 13:30:00",
        beacon: "NOPQRS456789",
        plate: "TN 09 STU",
        violations: 9,
      },
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
      {
        id: 2,
        timestamp: "2025-07-12 14:45:00",
        beacon: "HIJKLM890123",
        plate: "KL 19 ABC",
        violations: 4,
      },
      {
        id: 3,
        timestamp: "2025-07-12 13:30:00",
        beacon: "NOPQRS456789",
        plate: "TN 09 STU",
        violations: 9,
      },
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
      {
        id: 2,
        timestamp: "2025-07-12 14:45:00",
        beacon: "HIJKLM890123",
        plate: "KL 19 ABC",
        violations: 4,
      },
      {
        id: 3,
        timestamp: "2025-07-12 13:30:00",
        beacon: "NOPQRS456789",
        plate: "TN 09 STU",
        violations: 9,
      },
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
      {
        id: 2,
        timestamp: "2025-07-12 14:45:00",
        beacon: "HIJKLM890123",
        plate: "KL 19 ABC",
        violations: 4,
      },
      {
        id: 3,
        timestamp: "2025-07-12 13:30:00",
        beacon: "NOPQRS456789",
        plate: "TN 09 STU",
        violations: 9,
      },
      {
        id: 1,
        timestamp: "2025-07-12 15:20:00",
        beacon: "BCDEFG234567",
        plate: "KA 01 MNO",
        violations: 6,
      },
    ],
  },
  profiles: {
    "KL 19 ABC": {
      name: "Rahul Menon",
      dob: "1998-05-12",
      phone: "+91 9876543210",
      address: "Ernakulam, Kerala",
      maritalStatus: "Single",
      registeredPlates: ["KL 19 ABC", "KL 20 DEF", "KL 19 GHI"],
      recentScans: [
        { timestamp: "2025-07-12 14:30:00", location: "MG Road, Bangalore" },
        {
          timestamp: "2025-07-12 09:15:00",
          location: "Brigade Road, Bangalore",
        },
        {
          timestamp: "2025-07-11 18:45:00",
          location: "Koramangala, Bangalore",
        },
      ],
      recentViolations: [
        {
          timestamp: "2025-07-12 14:30:00",
          location: "MG Road, Bangalore",
          count: 8,
        },
        {
          timestamp: "2025-07-10 16:20:00",
          location: "Commercial Street, Bangalore",
          count: 3,
        },
        {
          timestamp: "2025-07-08 11:30:00",
          location: "Residency Road, Bangalore",
          count: 5,
        },
      ],
    },
    "KA 05 XYZ": {
      name: "Priya Sharma",
      dob: "1995-08-22",
      phone: "+91 9123456789",
      address: "Jayanagar, Bangalore",
      maritalStatus: "Married",
      registeredPlates: ["KA 05 XYZ", "KA 03 LMN"],
      recentScans: [
        { timestamp: "2025-07-12 13:45:00", location: "MG Road, Bangalore" },
        {
          timestamp: "2025-07-12 08:30:00",
          location: "Indiranagar, Bangalore",
        },
      ],
      recentViolations: [
        {
          timestamp: "2025-07-12 13:45:00",
          location: "MG Road, Bangalore",
          count: 3,
        },
        {
          timestamp: "2025-07-09 14:15:00",
          location: "Brigade Road, Bangalore",
          count: 2,
        },
      ],
    },
  },
};

let apiUrl = `https://django-api.sreedevss.me/api/`;

let currentCamera = null;
let currentPlate = null;

// Initialize the app
function init() {
  setupEventListeners();
  // Check if user is already logged in
  const isLoggedIn = sessionStorage.getItem("isLoggedIn");
  if (isLoggedIn === "true") {
    anime();
    showDashboard();
  } else {
    showPage("loginPage");
  }

  // Pre-fill username if remembered
  const rememberedUser = localStorage.getItem("rememberedUser");
  if (rememberedUser) {
    document.getElementById("username").value = rememberedUser;
    document.getElementById("rememberMe").checked = true;
  }
}

function setupEventListeners() {
  // Login form
  document.getElementById("loginForm").addEventListener("submit", handleLogin);

  // Search functionality
  document
    .getElementById("cameraSearch")
    .addEventListener("input", filterCameras);
  document
    .getElementById("violationSearch")
    .addEventListener("input", filterViolations);
}

async function handleLogin(e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;
  const rememberMe = document.getElementById("rememberMe").checked;

  try {
    const response = await fetch(`${apiUrl}login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      sessionStorage.setItem("isLoggedIn", "true");
      sessionStorage.setItem("username", username);

      if (rememberMe) {
        localStorage.setItem("rememberedUser", username);
      }

      // Animate success
      const loginBtn = document.querySelector(".login-btn");
      loginBtn.innerHTML = '<span class="btn-text">Success!</span>';
      loginBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";

      setTimeout(() => {
        anime();
        showDashboard();
      }, 1000);
    } else {
      showLoginError(data.message || "Invalid username or password");
    }
  } catch (error) {
    console.error("Login error:", error);
    showLoginError("An error occurred. Please try again.");
  }
}

function showLoginError(message) {
  // Remove existing error
  const existingError = document.querySelector(".login-error");
  if (existingError) {
    existingError.remove();
  }

  // Create error element
  const errorDiv = document.createElement("div");
  errorDiv.className = "login-error";
  errorDiv.style.cssText = `
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
                color: #fca5a5;
                padding: 12px 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 0.9rem;
                text-align: center;
            `;
  errorDiv.textContent = message;

  // Insert error above login button
  const loginBtn = document.querySelector(".login-btn");
  loginBtn.parentNode.insertBefore(errorDiv, loginBtn);

  // Remove error after 3 seconds
  setTimeout(() => {
    errorDiv.remove();
  }, 3000);
}

function showDashboard() {
  renderCameraGrid();
  showPage("page1");
}

function logout() {
  sessionStorage.removeItem("isLoggedIn");
  sessionStorage.removeItem("username");

  // Reset login form
  document.getElementById("loginForm").reset();
  const loginBtn = document.querySelector(".login-btn");
  loginBtn.innerHTML =
    '<span class="btn-text">Sign In</span><span class="btn-icon">→</span>';
  loginBtn.style.background =
    "linear-gradient(135deg, #a8edea 0%, #7dd3fc 100%)";

  showPage("loginPage");
}

async function renderCameraGrid() {
  const grid = document.getElementById("cameraGrid");
  grid.innerHTML = "";

  fetch(`${apiUrl}cameras/`)
    .then((response) => response.json())
    .then((cameras) => {
      cameras.forEach(async (camera) => {
        const res = await fetch(`${apiUrl}cameras/${camera.cam_id}/`);
        const data = await res.json();

        const card = document.createElement("div");
        card.className = "camera-card glass-card fade-in";
        card.onclick = () =>
          showViolations(camera.cam_id, camera.location_name, data.count);

        card.innerHTML = `
                      <div class="violations-badge">${data.count}</div>
                      <div class="camera-id">${camera.cam_id}</div>
                      <div class="camera-location">${camera.location_name}</div>
                      <div class="camera-coordinates">${camera.coordinates}</div>
                  `;

        grid.appendChild(card);
      });
    });
}

function filterCameras() {
  const searchTerm = document
    .getElementById("cameraSearch")
    .value.toLowerCase();
  const cards = document.querySelectorAll(".camera-card");

  cards.forEach((card) => {
    const text = card.textContent.toLowerCase();
    card.style.display = text.includes(searchTerm) ? "flex" : "none";
  });
}

function showViolations(id, location, violations) {
  currentCamera = id;

  document.getElementById("cameraTitle").textContent = `${id} - Violations`;
  document.getElementById(
    "cameraSubtitle"
  ).textContent = `${location} • ${violations} violations`;

  renderViolationsTable(id);
  showPage("page2");
}

async function renderViolationsTable(cameraId) {
  const tbody = document.getElementById("violationsTableBody");
  tbody.innerHTML = "";

  const allViolationsResponse = await fetch(`${apiUrl}violations/${cameraId}`);
  const allViolations = await allViolationsResponse.json();

  for (const violation of allViolations) {
    const res = await fetch(`${apiUrl}vehicles/${violation.chip}/`);
    const data = await res.json();

    const row = document.createElement("tr");
    row.onclick = () => showProfile(data.plate);

    row.innerHTML = `
                <td>${violation.violation_id}</td>
                <td>${violation.timestamp}</td>
                <td>${violation.chip}</td>
                <td>${data.plate_no}</td>
                <td><span class="violation-count">${allViolations.filter(v => v.chip === violation.chip).length}</span></td>
            `;

    tbody.appendChild(row);
  }
}

function filterViolations() {
  const searchTerm = document
    .getElementById("violationSearch")
    .value.toLowerCase();
  const rows = document.querySelectorAll(".violations-table tbody tr");

  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(searchTerm) ? "table-row" : "none";
  });
}

function showProfile(plate) {
  currentPlate = plate;
  const profile = mockData.profiles[plate];

  if (!profile) {
    alert("Profile not found for this vehicle");
    return;
  }

  // Update profile information
  document.getElementById("profileImage").textContent = profile.name
    .split(" ")
    .map((n) => n[0])
    .join("");
  document.getElementById("profileName").textContent = profile.name;
  document.getElementById("profileDob").textContent = profile.dob;
  document.getElementById("profilePhone").textContent = profile.phone;
  document.getElementById("profileAddress").textContent = profile.address;
  document.getElementById("profilePlate").textContent = plate;
  document.getElementById("profileMarital").textContent = profile.maritalStatus;

  // Render vehicle buttons
  const vehicleButtons = document.getElementById("vehicleButtons");
  vehicleButtons.innerHTML = "";
  profile.registeredPlates.forEach((plateNum) => {
    const button = document.createElement("button");
    button.className = "vehicle-btn";
    button.textContent = plateNum;
    button.onclick = () => showProfile(plateNum);
    vehicleButtons.appendChild(button);
  });

  // Render recent scans
  const scansContainer = document.getElementById("recentScans");
  scansContainer.innerHTML = "";
  profile.recentScans.forEach((scan) => {
    const scanItem = document.createElement("div");
    scanItem.className = "scan-item";
    scanItem.innerHTML = `
                    <div class="item-time">${scan.timestamp}</div>
                    <div class="item-location">${scan.location}</div>
                `;
    scansContainer.appendChild(scanItem);
  });

  // Render recent violations
  const violationsContainer = document.getElementById("recentViolations");
  violationsContainer.innerHTML = "";
  profile.recentViolations.forEach((violation) => {
    const violationItem = document.createElement("div");
    violationItem.className = "violation-item";
    violationItem.innerHTML = `
                    <div class="item-time">${violation.timestamp}</div>
                    <div class="item-location">${violation.location}</div>
                    <div class="violation-count">${violation.count} violations</div>
                `;
    violationsContainer.appendChild(violationItem);
  });

  showPage("page3");
}

function showPage(pageId) {
  // Hide all pages
  document.querySelectorAll(".page").forEach((page) => {
    page.classList.remove("active");
  });

  // Show selected page
  const targetPage = document.getElementById(pageId);
  targetPage.classList.add("active");

  // Add fade-in animation
  targetPage.classList.add("fade-in");
  setTimeout(() => {
    targetPage.classList.remove("fade-in");
  }, 600);
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", init);

function anime() {
  // Only target elements within the anime container
  var animeContainer = document.querySelector(".anime");
  const mainContainer = document.querySelector(".container1");
  mainContainer.style.display = "block";
  mainContainer.style.opacity = "1";
  mainContainer.style.transition = "transform 6s ease-in-out";
  mainContainer.style.transform = "scale(1.5)";
  if (!animeContainer) return; // Exit if anime container doesn't exist

  var w = window.innerWidth;
  var h = window.innerHeight;
  var boxAmount = 10;
  if (w > 1000) {
    boxAmount += 10;
  } else if (w < 500) {
    boxAmount -= 5;
  }

  // Scope grid selection to anime container only
  var grid = animeContainer.querySelector(".grid");
  for (var i = 0; i < boxAmount; i++) {
    var newDiv = document.createElement("div");
    newDiv.className = "ani ani" + i;
    grid.appendChild(newDiv);

    var num = Math.random() * h + 1;
    var num2 = Math.random() * w + 1;
    var aniElement = animeContainer.querySelector(".ani" + i);
    aniElement.style.top = num + "px";
    aniElement.style.left = num2 + "px";
  }
  mainContainer.classList.add("op");

  setTimeout(function () {
    var shapeContain = animeContainer.querySelector(".shape-contain");
    shapeContain.innerHTML +=
      '<div class="container1">' +
      '<div class="p1"></div>' +
      '<div class="p2"></div>' +
      "</div>";
  }, 500);

  setTimeout(function () {
    var container = animeContainer.querySelector(".container1");
    container.innerHTML += '<div class="p3"></div>';
  }, 750);

  setTimeout(function () {
    var container = animeContainer.querySelector(".container1");
    container.innerHTML += '<div class="p4"></div><div class="p5"></div>';
  }, 800);

  setTimeout(function () {
    var container = animeContainer.querySelector(".container1");
    container.innerHTML +=
      '<div class="p4"></div><div class="p6"></div><div class="p7"></div><div class="p23"></div><div class="p32"></div>';
  }, 820);

  setTimeout(function () {
    var container = animeContainer.querySelector(".container1");
    container.innerHTML +=
      '<div class="p33"></div><div class="p34"></div><div class="p35"></div><div class="p8"></div><div class="p9"></div><div class="p10"></div><div class="p11"></div><div class="p12"></div><div class="p13"></div><div class="p14"></div><div class="p15"></div><div class="p16"></div><div class="p17"></div><div class="p18"></div><div class="p19"></div><div class="p20"></div><div class="p21"></div><div class="p22"></div>';
  }, 870);

  setTimeout(function () {
    var container = animeContainer.querySelector(".container1");
    container.innerHTML += "";
  }, 880);
}
