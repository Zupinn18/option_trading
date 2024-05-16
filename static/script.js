
let strikeSet = {}; // unique strike values

async function fetchDataFromCSV() {
    try {
        const response = await fetch('./static/updated_NFO.csv');
        if (!response.ok) {
            throw new Error('Failed to fetch CSV file');
        }
        const csvData = await response.text();
        const rows = csvData.split('\n').slice(1); // Skip header row
        const dataArray = rows.map(row => {
            const [strike, optionType, token] = row.split(',');
            if (!isNaN(parseFloat(strike))) {
                return { strike: parseFloat(strike), optionType, token: parseInt(token) };
            }
        }).filter(Boolean); // Filter out NaN values
        return dataArray;
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
        if (data[token] && data[token].data && data[token].data.lp) {
            return data[token].data.lp;
        } else {
            throw new Error('LP value not found in response');
        }
    } catch (error) {
        console.error(error);
        return 'N/A';
    }
}

async function fetchDataAndUpdate() {
    const csvData = await fetchDataFromCSV();
    const optionsData = [];
    for (const item of csvData) {
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
    putList.innerHTML = '';
    
    optionsData.forEach(option => {
        if (option.optionType === 'CE') {
            callList.innerHTML += `<li>${option.lp}</li>`;
        } else if(option.optionType === 'PE') {
            putList.innerHTML += `<li>${option.lp}</li>`;
        }
    });
    
    // Update strike values only if they are not already present
    optionsData.forEach(option => {
        if (!strikeSet[option.strike]) {
            strikeList.innerHTML += `<li>${option.strike}</li>`;
            strikeSet[option.strike] = true; // Mark the strike value as added
        }
    });
}

setInterval(fetchDataAndUpdate, 5000);
fetchDataAndUpdate(); // Initial fetch
