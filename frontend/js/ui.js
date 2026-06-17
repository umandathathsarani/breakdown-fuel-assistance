const UI = {
    setupImagePreview: () => {
        const fileInput = document.getElementById('dashboard-img');
        const uploadBtn = document.getElementById('upload-btn');
        const previewBox = document.getElementById('image-preview');

        uploadBtn.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewBox.innerHTML = `<img src="${e.target.result}" alt="Dashboard Preview" style="display:block;">`;
                    uploadBtn.textContent = "Change Image";
                }
                reader.readAsDataURL(file);
            }
        });
    }
};