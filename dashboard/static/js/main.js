const socket = io();

socket.on('telemetry', data => {
    const { subsystem, status, payload } = data;
    const grid = document.querySelector(".grid");
    let panel = document.getElementById(subsystem);

    // Create panel if it doesn't exist
    if (!panel) {
        panel = document.createElement("div");
        panel.className = "panel";
        panel.id = subsystem;

        const label = document.createElement("span");
        label.className = "panel-label";
        label.textContent = subsystem;

        const statusLight = document.createElement("div");
        statusLight.className = getStatusClass(status);
        statusLight.classList.add("status-light");

        panel.appendChild(label);
        panel.appendChild(statusLight);
        grid.appendChild(panel);
    } else {
        // Update existing panel
        const light = panel.querySelector(".status-light");
        if (light) light.className = `status-light ${getStatusClass(status)}`;
    }

    updateMainStatus();
});

function getStatusClass(status) {
    switch (status) {
        case "nominal": return "status-subsystem-green";
        case "emergency": return "status-subsystem-red";
        default: return "status-subsystem-yellow";
    }
}

function updateMainStatus() {
    const panels = document.getElementsByClassName("panel");
    const statusContainer = document.getElementById("status-container");

    if (panels.length < 7) {
        statusContainer.className = "status-main-yellow";
        return;
    } else {
        document.getElementById("status-text").textContent = "Subsystems Online";
    }

    const anyRed = Array.from(panels).some(panel =>
        panel.querySelector(".status-subsystem-red")
    );

    statusContainer.className = anyRed
        ? "status-main-red"
        : "status-main-green";
}
