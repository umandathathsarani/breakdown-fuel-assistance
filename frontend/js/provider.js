document.addEventListener('DOMContentLoaded', () => {
    const queueContainer = document.getElementById('queue-container');

    const fetchIncidentQueue = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/providers/requests');
            const tickets = await response.json();
            renderQueue(tickets);
        } catch (error) {
            console.error("Failed syncing data streams from API:", error);
        }
    };

    const renderQueue = (tickets) => {
        if (tickets.length === 0) {
            queueContainer.innerHTML = '<p style="text-align:center; color:#999;">No active road emergencies registered.</p>';
            return;
        }

        queueContainer.innerHTML = tickets.map(ticket => `
            <div class="ticket-card ${ticket.status}">
                <div class="meta-row">
                    <span>Ticket ID: #${ticket.ticket_id}</span>
                    <span>Received: ${ticket.timestamp}</span>
                </div>
                <h3>${ticket.diagnosis}</h3>
                <p style="margin: 0.5rem 0;"><strong>Location:</strong> ${ticket.location}</p>
                <p><strong>AI Reliability Threshold:</strong> ${ticket.confidence}</p>
                <p><strong>Current Status:</strong> <span class="badge">${ticket.status}</span></p>
                ${ticket.status === 'Pending' ? 
                    `<button class="btn-claim" onclick="claimIncident(${ticket.ticket_id})">Accept & Dispatch Unit</button>` : 
                    ''
                }
            </div>
        `).join('');
    };

    window.claimIncident = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/providers/accept/${id}`, { method: 'POST' });
            if (response.ok) {
                fetchIncidentQueue(); 
            }
        } catch (error) {
            alert("Error sending transmission payload.");
        }
    };

    fetchIncidentQueue();
    setInterval(fetchIncidentQueue, 3000);
});