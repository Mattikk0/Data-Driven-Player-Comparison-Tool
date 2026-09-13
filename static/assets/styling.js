function parseComparableValue(value) {
    if (value === null || value === undefined) return Number.NaN;
    const normalized = String(value).replace(/[^0-9.\-]/g, '');
    if (!normalized || normalized === '-' || normalized === '.') return Number.NaN;
    const parsedValue = Number(normalized);
    return Number.isFinite(parsedValue) ? parsedValue : Number.NaN;
}

function valueColoring(table, searchedPlayerValue){
    const rows = Array.from(table.rows);
    rows.forEach((row) => {
        if (!row || !row.cells || row.cells.length <= 4) return;
        const cell = row.cells[4];
        if (!cell) return;
        const content = cell.innerText.trim();
        const value = parseComparableValue(content);
        if (!Number.isNaN(value) && Number.isFinite(value)) {
            if (value > searchedPlayerValue) {
                cell.style.color = "rgb(168, 0, 0)";
            } else if (value < searchedPlayerValue) {
                cell.style.color = "rgb(0, 159, 0)";
            }
        }
    });
}

function similarityColoring(table){
    const rows = Array.from(table.rows);
    rows.forEach((row) => {
        if (!row || !row.cells || row.cells.length <= 5) return;
        const cell = row.cells[5];
        if (!cell) return;
        const content = cell.innerText.trim();
        const sim = parseComparableValue(content);
        if (!Number.isNaN(sim) && Number.isFinite(sim)) {
            cell.style.color = pickSimilarityColor(sim);
        }
    });
}

function pickSimilarityColor(sim_value){
    if(sim_value >= 0.9){
        return "rgb(0, 89, 0)"
    }
    if(sim_value >= 0.8 && sim_value < 0.9){
        return "rgb(0, 155, 0)"
    }
    if(sim_value >= 0.6 && sim_value < 0.8){
        return "rgb(67, 191, 0)"
    }
    if(sim_value >= 0.4 && sim_value < 0.6){
        return "rgb(152, 198, 0)"
    }
    if(sim_value <= -0.9){
        return "rgb(88, 0, 0)"
    }
    if(sim_value <= -0.8 && sim_value > -0.9){
        return "rgb(160, 0, 0)"
    }
    
    if(sim_value <= -0.6 && sim_value > -0.8){
        return "rgb(217, 0, 0)"
    }
    if(sim_value <= -0.4 && sim_value > -0.6){
        return "rgb(206, 96, 0)"
    }

}
window.parseComparableValue = parseComparableValue;
window.valueColoring = valueColoring;
window.similarityColoring = similarityColoring;