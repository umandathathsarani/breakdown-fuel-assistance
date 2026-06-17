const API = {
    diagnoseImage: async (imageFile) => {
        const formData = new FormData();
        formData.append('image', imageFile);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/diagnose', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error("Server responded with an error.");
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error("API Connection Error:", error);
            return null;
        }
    }
};