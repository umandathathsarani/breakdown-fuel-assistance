document.addEventListener('DOMContentLoaded', () => {
    UI.setupImagePreview();

    const form = document.getElementById('breakdown-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const location = document.getElementById('location').value;
        const imageFile = document.getElementById('dashboard-img').files[0];

        if (!imageFile) {
            UI.showModal("Missing Information", "Please upload a picture of your dashboard warning light.");
            return;
        }

        console.log("Ready to send to Python backend:", location, imageFile.name);
        
        UI.showModal("Success!", "Frontend is working! Next step: Connect to Python API.");
    });
});