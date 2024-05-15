async function fetchDataFromCSV() {
    try {
        const response = await fetch('updated_NFO.csv');
        if (!response.ok) {
            throw new Error('Failed to fetch CSV file');
        }
        const csvData = await response.text();
        const rows = csvData.split('\n').slice(1);
        const optionsData = rows.map(row => {
            const [strike, optionType, token] = row.split(',');
            return { strike: parseFloat(strike), optionType, token: parseInt(token) };
        });
        return optionsData;
    } catch (error) {
        console.error(error);
        return [];
    }
}

async function fetchLP(token) {
    try {
        const response = await fetch(`http://127.0.0.1:8009/get_data?token=${token}`);
        if (!response.ok) {
            throw new Error('Failed to fetch LP value');
        }
        const data = await response.json();
        if (!data[token] || !data[token].data || !data[token].data.lp) {
            throw new Error('LP value not found in response');
        }
        return data[token].data.lp;
    } catch (error) {
        console.error(error);
        return 'N/A';
    }
}

async function fetchDataAndUpdate() {
    const data = await fetchDataFromCSV();
    const optionsData = [];
    for (const item of data) {
        const lp = await fetchLP(item.token);
        optionsData.push({ strike: item.strike, optionType: item.optionType, lp: lp });
    }
    updateOptions(optionsData);
}

function updateOptions(optionsData) {
    const callList = document.getElementById('call-list');
    const strikeList = document.getElementById('strike-list');
    const putList = document.getElementById('put-list');
    
    callList.innerHTML = '';
    strikeList.innerHTML = '';
    putList.innerHTML = '';
    
    optionsData.forEach(option => {
        if (option.optionType === 'CE') {
            callList.innerHTML += `<li>${option.lp}</li>`;
        } else {
            putList.innerHTML += `<li>${option.lp}</li>`;
        }
        strikeList.innerHTML += `<li>${option.strike}</li>`;
    });
}

setInterval(fetchDataAndUpdate, 5000);
fetchDataAndUpdate(); // Initial fetch
