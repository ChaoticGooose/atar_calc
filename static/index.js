async function fetchScaling(subject, rawScore) {
    const response = await fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            subject: subject,
            rawScore: rawScore
        })
    });
    return response.json();
}

const table = document.getElementsByTagName('table')[0];
const rows = table.getElementsByTagName('tr');

for (let i = 1; i < rows.length; i++) {
    // Element selectors
    const row = rows[i];
    const subject_obj = row.getElementsByTagName('select')[0];
    const score_obj = row.getElementsByTagName('input')[0];

    score_obj.addEventListener('input', function() {
        // Value Selectors
        const subject = subject_obj.options[subject_obj.selectedIndex].text;
        const subject_id = subject_obj.value;
        const score = score_obj.value

        // Do nothing if there is no subject selected
        if (subject_id === '0') {
            return;
        }

        // Send data to the server
        fetchScaling(subject, score).then(data => {
            for (const year in data) {
                // Get p tag with the year and matching row
                const p = row.getElementsByClassName(year)[0];
                p.innerHTML = data[year];
            }
        }).catch(error => { // Clear the p tags if there is an error and log the error
            console.warn(error);
            console.warn('Likley an empty input');
            const p = row.getElementsByTagName('p');
            for (let i = 0; i < p.length; i++) {
                p[i].innerHTML = '';
            }
        });
    });
}
