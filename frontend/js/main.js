document.addEventListener('DOMContentLoaded', () => {
    UI.setupImagePreview();

    const form = document.getElementById('breakdown-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const location = document.getElementById('location').value;
        const imageFile = document.getElementById('dashboard-img').files[0];

        if (!imageFile) {
            UI.showModal("Missing Information", "Please upload a picture of your dashboard warning light.");
            return;
        }

        UI.showModal("Analyzing...", "Sending dashboard image to AI for diagnosis.");

        const result = await API.diagnoseImage(imageFile);

        if (result && result.status === "success") {
            const successMessage = `${result.message} (Confidence: ${result.confidence * 100}%)`;
            UI.showModal("Diagnosis Complete", successMessage);
        } else {
            UI.showModal("Error", "Failed to connect to the AI server. Is Python running?");
        }
    });
});