// Mock JSON data
const mockData = {
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

let currentCamera = null;
let currentPlate = null;

// Initialize the app
function init() {
  renderCameraGrid();
  setupEventListeners();
}

function setupEventListeners() {
  document
    .getElementById("cameraSearch")
    .addEventListener("input", filterCameras);
  document
    .getElementById("violationSearch")
    .addEventListener("input", filterViolations);
}

function renderCameraGrid() {
  const grid = document.getElementById("cameraGrid");
  grid.innerHTML = "";

  mockData.cameras.forEach((camera) => {
    const card = document.createElement("div");
    card.className = "camera-card glass-card fade-in";
    card.onclick = () => showViolations(camera.id);

    card.innerHTML = `
                    <div class="violations-badge">${camera.violations}</div>
                    <div class="camera-id">${camera.id}</div>
                    <div class="camera-location">${camera.location}</div>
                    <div class="camera-coordinates">${camera.coordinates}</div>
                `;

    grid.appendChild(card);
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

function showViolations(cameraId) {
  currentCamera = cameraId;
  const camera = mockData.cameras.find((c) => c.id === cameraId);

  document.getElementById(
    "cameraTitle"
  ).textContent = `${camera.id} - Violations`;
  document.getElementById(
    "cameraSubtitle"
  ).textContent = `${camera.location} • ${camera.violations} violations`;

  renderViolationsTable(cameraId);
  showPage("page2");
}

function renderViolationsTable(cameraId) {
  const tbody = document.getElementById("violationsTableBody");
  tbody.innerHTML = "";

  const violations = mockData.violations[cameraId] || [];

  violations.forEach((violation) => {
    const row = document.createElement("tr");
    row.onclick = () => showProfile(violation.plate);

    row.innerHTML = `
                    <td>${violation.id}</td>
                    <td>${violation.timestamp}</td>
                    <td>${violation.beacon}</td>
                    <td>${violation.plate}</td>
                    <td><span class="violation-count">${violation.violations}</span></td>
                `;

    tbody.appendChild(row);
  });
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
