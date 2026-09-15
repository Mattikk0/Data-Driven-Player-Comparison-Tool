const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('name-input');
const bestResemblanceTable = document.getElementById('most-similar-table');
const worstResemblanceTable = document.getElementById('least-similar-table');
const playerInfoTable = document.getElementById('player-info-table');
const searchedPlayerImage = document.getElementById('searched-player-image');
const playerLoader = document.getElementById('player-info-loader');
const resultLoader = document.getElementById('result-loader');
const greatestSimilarity = document.getElementById('greatest-similarity');
const leastSimilarity = document.getElementById('least-similarity');
const ls_a = document.querySelector('#least-similarity a');
const gs_a = document.querySelector('#greatest-similarity a');
const searchPlayerContainer = document.getElementById('searched-player-container');
const resultContainer = document.getElementById('result-container');

async function playerInfo(){
    const data = { player_name: searchInput.value.trim() };
    try {
        const response = await fetch('/player_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || `Search failed with status ${response.status}`);
        }
        const row = playerInfoTable.insertRow();
        row.insertCell(0).textContent = result.name;
        row.insertCell(1).textContent = result.position;
        row.insertCell(2).textContent = result.age;
        row.insertCell(3).textContent = result.team;
        row.insertCell(4).textContent = result.value;
        searchPlayerContainer.style.display = "flex";
        playerInfoTable.style.display = "flex";
        searchedPlayerImage.src = result.image_url;
        playerLoader.style.display = "none";

        return parseComparableValue(result.value);
    } catch (error) {
        console.error('Could not fetch player info:', error);
        playerLoader.style.display = "none";
        return Number.NaN;
    }
}

async function dataExchange(){
    const data = { player_name: searchInput.value.trim() };
    try {
         const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || `Search failed with status ${response.status}`);
        }
        const { least, most } = result;
        most.forEach(player => {
            const row = bestResemblanceTable.insertRow();
            row.insertCell(0).textContent = player.name;
            row.insertCell(1).textContent = player.position;
            row.insertCell(2).textContent = player.age;
            row.insertCell(3).textContent = player.team;
            row.insertCell(4).textContent = player.value;
            row.insertCell(5).textContent = player.similarity;
            
        });
        least.forEach(player => {
            const row = worstResemblanceTable.insertRow();
            row.insertCell(0).textContent = player.name;
            row.insertCell(1).textContent = player.position;
            row.insertCell(2).textContent = player.age;
            row.insertCell(3).textContent = player.team;
            row.insertCell(4).textContent = player.value;
            row.insertCell(5).textContent = player.similarity;
            
        });
        resultContainer.style.display = "flex";
        worstResemblanceTable.style.display = "none";
        bestResemblanceTable.style.display = "flex";
        resultLoader.style.display = "none";
    }catch(error){
        console.error('Could not exchange data:', error);
        resultLoader.style.display = "none";
    }
}

searchButton.addEventListener('click', async (event) => {
    event.preventDefault();
    if (searchInput.value.trim() !== '') {
        if (resultContainer.style.display === "flex") {
            resetTable(bestResemblanceTable);
            resetTable(worstResemblanceTable);
            resetTable(playerInfoTable);
            searchPlayerContainer.style.display = "none";
            resultContainer.style.display = "none";
        }
        playerLoader.style.display = "block";
        resultLoader.style.display = "block";
        
    ////////////////////////////////////////////////////////    
        const startTime = performance.now();
////////////////////////////////////////////////////////////


        const searchedPlayerValue = await playerInfo();
        await dataExchange();

////////////////////////////////////////////////////////////
        const endTime = performance.now();
        const duration = (endTime - startTime);
        console.log(`Całkowity czas wykonania: ${duration.toFixed(3)} ms`);
///////////////////////////////////////////////////////////

        if (!Number.isNaN(searchedPlayerValue) && Number.isFinite(searchedPlayerValue)) {
            valueColoring(bestResemblanceTable, searchedPlayerValue);
            valueColoring(worstResemblanceTable, searchedPlayerValue);
        }
        similarityColoring(worstResemblanceTable);
        similarityColoring(bestResemblanceTable);
    }
});

function resetTable(table){
    table.style.display = "none";
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
}

leastSimilarity.addEventListener('click', () => {
    if(leastSimilarity.style.backgroundColor !== "rgba(0, 0, 0, 1)"){
        leastSimilarity.style.backgroundColor = "rgba(0, 0, 0, 1)";
        greatestSimilarity.style.backgroundColor = "rgba(0, 0, 0, 0)";
        ls_a.style.color = "rgba(255, 255, 255, 0.8)";
        gs_a.style.color = "rgba(0, 0, 0, 1)";
        bestResemblanceTable.style.display = "none";
        worstResemblanceTable.style.display = "flex";
    }
});

greatestSimilarity.addEventListener('click', () => {
    if(greatestSimilarity.style.backgroundColor !== "rgba(0, 0, 0, 1)"){
        greatestSimilarity.style.backgroundColor = "rgba(0, 0, 0, 1)";
        leastSimilarity.style.backgroundColor = "rgba(0, 0, 0, 0)";
        gs_a.style.color = "rgba(255, 255, 255, 0.8)";
        ls_a.style.color = "rgba(0, 0, 0, 1)";
        worstResemblanceTable.style.display = "none";
        bestResemblanceTable.style.display = "flex";
    }
});