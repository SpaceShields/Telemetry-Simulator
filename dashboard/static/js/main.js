const socket = io();

const grid = document.getElementById("subsystem-grid") || document.querySelector(".grid");
const statusContainer = document.getElementById("status-container");
const statusText = document.getElementById("status-text");

const subsystemPanels = {};
const subsystemTimestamps = {};

function getStatusClass(status) {
    switch (status) {
        case "nominal": return "status-subsystem-green";
        case "emergency": return "status-subsystem-red";
        default: return "status-subsystem-yellow";
    }
}

function createStatusLight(status) {
    const light = document.createElement("div");
    light.className = `status-light ${getStatusClass(status)}`;
    return light;
}

function createPanel(subsystem) {
    const panel = document.createElement("div");
    panel.className = "panel";
    panel.id = `panel-${subsystem}`;
    panel.dataset.status = "unknown";

    const label = document.createElement("h2");
    label.textContent = subsystem.toUpperCase();
    label.className = "panel-label";

    const statusLight = createStatusLight("unknown");
    statusLight.classList.add("status-light");

    const timeInfo = document.createElement("p");
    timeInfo.className = "panel-timestamp";
    timeInfo.textContent = "--";

    const seqInfo = document.createElement("p");
    seqInfo.className = "panel-sequence";
    seqInfo.textContent = "#--";

    // const detailsLink = document.createElement("a");
    // detailsLink.href = `/subsystem/${subsystem}`;
    // detailsLink.className = "panel-link";
    // detailsLink.textContent = "View details →";

    panel.append(label, statusLight, timeInfo, seqInfo);
    panel.addEventListener('click', () => {
            window.location.href = `/${subsystem}`;
        });
    grid.appendChild(panel);
    subsystemPanels[subsystem] = panel;

    return panel;
}

function updateOverallStatus() {
    const total = Object.values(subsystemPanels).length;
    const red = Object.values(subsystemPanels).filter(p => p.dataset.status === "emergency").length;

    if (total < 7) {
        statusContainer.className = "status-main-yellow";
        statusText.textContent = "partial link";
    } else if (red > 0) {
        statusContainer.className = "status-main-red";
        statusText.textContent = "emergency";
    } else {
        statusContainer.className = "status-main-green";
        statusText.textContent = "nominal";
    }
}

function updatePanel(packet) {
    const { subsystem, timestamp, status, sequence_count, data  } = packet;
    const currentTimestamp = Date.now();
    subsystemTimestamps[subsystem] = currentTimestamp;

    const panel = subsystemPanels[subsystem] || createPanel(subsystem);
    panel.dataset.status = status;

    // Update status light
    const existingLight = panel.querySelector(".status-light");
    if (existingLight) {
        existingLight.className = `status-light ${getStatusClass(status)}`;
    }

    // Update sequence
    const seqInfo = panel.querySelector(".panel-sequence");
    if (seqInfo) {
        seqInfo.textContent = `#${sequence_count || "--"}`;
    }

    updateOverallStatus();
}

function updateTimestamps() {
    const now = Date.now();
    for (const [subsystem, ts] of Object.entries(subsystemTimestamps)) {
        const panel = subsystemPanels[subsystem];
        if (!panel) continue;

        const elapsedSec = Math.floor((now - ts) / 1000);
        const timeInfo = panel.querySelector(".panel-timestamp");
        if (timeInfo) {
            timeInfo.textContent = `${elapsedSec}s ago`;
        }
    }
    requestAnimationFrame(updateTimestamps);
}

socket.on("telemetry", data => {
    updatePanel(data);
});

requestAnimationFrame(updateTimestamps);
