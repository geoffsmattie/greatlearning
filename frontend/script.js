
document.getElementById('predictionForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        // Convert numeric fields to numbers
        if (['Product_Weight', 'Product_Allocated_Area', 'Product_MRP', 'Store_Age_Years'].includes(key)) {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    });

    // IMPORTANT: Replace this with wherever your backend/ Flask API ends up
    // running (e.g. a Render.com free web service), or leave it pointing at
    // localhost for local testing. Note: the live app deployed in the
    // "Deployment - Live App" section below is a self-contained Streamlit
    // app that does not use this HTML/JS frontend at all.
    const API_URL = 'http://127.0.0.1:7860/v1/predict'; // Default for local Flask app via gunicorn

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}, Details: ${errorText}`);
        }

        const result = await response.json();
        document.getElementById('result').innerText = `Predicted Sales: $${result.Sales.toFixed(2)}`;
    } catch (error) {
        console.error('Error during prediction:', error);
        document.getElementById('result').innerText = `Error: ${error.message}`;
    }
});
