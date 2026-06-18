document.addEventListener('DOMContentLoaded', () => {
    UI.setupImagePreview();
    UI.setupServiceToggle();

    const form = document.getElementById('breakdown-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const serviceType = document.querySelector('input[name="service_type"]:checked').value;
        const locationInput = document.getElementById('location').value;
        const formData = new FormData();
        formData.append('location', locationInput);

        let apiUrl = '';

        if (serviceType === 'breakdown') {
            const imageFile = document.getElementById('dashboard-img').files[0];
            if (!imageFile) {
                UI.showModal("Missing Information", "Please upload a picture of your dashboard warning light.");
                return;
            }
            formData.append('image', imageFile);
            apiUrl = 'http://127.0.0.1:8000/api/diagnose';
            UI.showModal("Analyzing & Dispatching...", "Processing telemetry...");
            
        } else if (serviceType === 'fuel') {
            const fuelType = document.getElementById('fuel-type').value;
            const amount = document.getElementById('fuel-amount').value;
            if (!amount) {
                UI.showModal("Missing Information", "Please specify the amount of liters needed.");
                return;
            }
            formData.append('fuel_type', fuelType);
            formData.append('amount', amount);
            apiUrl = 'http://127.0.0.1:8000/api/fuel';
            UI.showModal("Dispatching...", "Routing fuel request to local operators.");
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.status === "success") {
                UI.showModal(
                    "Assistance Dispatched", 
                    `${result.message}`
                );
            } else {
                UI.showModal("Error", "Failed to submit request.");
            }
        } catch (error) {
            UI.showModal("Connection Error", "Could not connect to server framework.");
        }
    });
});