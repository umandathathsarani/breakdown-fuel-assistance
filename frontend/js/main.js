document.addEventListener('DOMContentLoaded', () => {
    UI.setupImagePreview();

    const form = document.getElementById('breakdown-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const locationInput = document.getElementById('location').value;
        const imageFile = document.getElementById('dashboard-img').files[0];

        if (!imageFile) {
            UI.showModal("Missing Information", "Please upload a picture of your dashboard warning light.");
            return;
        }

        UI.showModal("Analyzing & Dispatching...", "Processing dashboard telemetry and routing to local operators.");

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('location', locationInput);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/diagnose', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.status === "success") {
                UI.showModal(
                    "Assistance Dispatched", 
                    `AI Diagnosis: ${result.ticket.diagnosis} (${result.ticket.confidence} confidence). Help has been called to ${result.ticket.location}.`
                );
            } else {
                UI.showModal("Error", "Failed to submit request.");
            }
        } catch (error) {
            UI.showModal("Connection Error", "Could not connect to server framework.");
        }
    });
});