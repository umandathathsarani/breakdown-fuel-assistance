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
    },

    setupServiceToggle: () => {
        const radios = document.querySelectorAll('input[name="service_type"]');
        const breakdownSection = document.getElementById('breakdown-section');
        const fuelSection = document.getElementById('fuel-section');

        radios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                if (e.target.value === 'breakdown') {
                    breakdownSection.style.display = 'block';
                    fuelSection.style.display = 'none';
                } else {
                    breakdownSection.style.display = 'none';
                    fuelSection.style.display = 'block';
                }
            });
        });
    },

    showModal: (title, message) => {
        const modal = document.getElementById('custom-modal');
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-message').textContent = message;

        modal.classList.remove('hidden');

        document.getElementById('modal-close-btn').onclick = () => {
            modal.classList.add('hidden');
        };
    }

};