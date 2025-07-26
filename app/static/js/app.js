const apiBaseUrl = '/api';

// Fetch api to get current servers
async function fetchServers() {
    const res = await fetch(apiBaseUrl + '/servers');
    return res.json();
}

// Add a server with optional credentials (will be validated by backend)
async function addServer(ip, username, password) {
    const res = await fetch(apiBaseUrl + '/servers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip, username, password })
    });
    return res.json();
}

// Remove a server
async function removeServer(id) {
    const res = await fetch(apiBaseUrl + `/servers/${id}`, {
        method: 'DELETE'
    });
    return res.json();
}

// Set global credentials for flashing
async function setCredentials(username, password) {
    const res = await fetch(apiBaseUrl + '/credentials', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    return res.json();
}

// Set firmware package URL
async function setFirmwareUrl(url) {
    const res = await fetch(apiBaseUrl + '/firmware/url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    });
    return res.json();
}

// Start firmware flashing asynchronously
async function startFlashing() {
    const res = await fetch(apiBaseUrl + '/flash/start', {
        method: 'POST'
    });
    return res.json();
}

// Helper to create a row in the server status table
function createServerTableRow(server) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${server.ip}</td>
        <td>${server.status || 'N/A'}</td>
        <td>${server.progress !== undefined ? server.progress + '%' : '0%'}</td>
        <td>${server.message || ''}</td>
        <td><button class="remove-btn" data-id="${server.id}">Remove</button></td>
    `;
    return tr;
}

// Refresh server list and display status table
async function refreshServerList() {
    const servers = await fetchServers();
    const tbody = document.querySelector('#statusTable tbody');
    tbody.innerHTML = '';
    servers.forEach(server => {
        const row = createServerTableRow(server);
        tbody.appendChild(row);
    });

    // Attach remove button handlers
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.onclick = async (e) => {
            const serverId = e.target.getAttribute('data-id');
            await removeServer(serverId);
            await refreshServerList();
        };
    });
}

// Event listeners binding
document.getElementById('addServerBtn').addEventListener('click', async () => {
    const ipInput = document.getElementById('serverIpInput');
    const usernameInput = document.getElementById('addServerUsername');
    const passwordInput = document.getElementById('addServerPassword');

    const ip = ipInput.value.trim();
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!ip) {
        alert('Please enter a server IP');
        return;
    }

    const result = await addServer(ip, username, password);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert(result.message);
        ipInput.value = '';
        usernameInput.value = '';
        passwordInput.value = '';
        await refreshServerList();
    }
});

document.getElementById('setCredsBtn').addEventListener('click', async () => {
    const username = document.getElementById('usernameInput').value.trim();
    const password = document.getElementById('passwordInput').value.trim();

    if (!username || !password) {
        alert('Enter both username and password');
        return;
    }

    const res = await setCredentials(username, password);
    alert(res.message || 'Global credentials set');
});

document.getElementById('setFirmwareUrlBtn').addEventListener('click', async () => {
    const url = document.getElementById('firmwareUrlInput').value.trim();

    if (!url) {
        alert('Enter firmware URL');
        return;
    }

    const res = await setFirmwareUrl(url);
    alert(res.message || 'Firmware URL set');
});

document.getElementById('flashAllBtn').addEventListener('click', async () => {
    const res = await startFlashing();
    alert(res.message || 'Started flashing');
    setTimeout(refreshServerList, 2000); // Refresh after 2 seconds to see initial status
});

// Initial load on page ready
refreshServerList();
setInterval(refreshServerList, 5000);