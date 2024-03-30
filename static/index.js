async function fetchData(rawScore, subject) {
    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rawScore, subject })
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching scaling data:', error);
        return null;
    }
}

// Document elements
const selects = document.querySelectorAll('select[name^="subject"]');
const inputs = document.querySelectorAll('input[name^="raw"]');

// Attach event listeners to all inputs
inputs.forEach(input => {
    input.addEventListener('input', async () => {
        // Get input data
        const select = document.querySelector(`select[name^="subject"]`);
        const subject = select.value;
        const rawScore = input.value;

        // fetch data
        const data = await fetchData(rawScore, select.value);
        console.log(data);
    });
});

