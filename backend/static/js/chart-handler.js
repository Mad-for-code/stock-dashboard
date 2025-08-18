let stockChart = null;

fetch("/companies")
    .then(res => res.json())
    .then(companies => {
    const list = document.getElementById("company-list");
    companies.forEach(company => {
        const li = document.createElement("li");
        li.textContent = company.name;
        li.dataset.ticker = company.ticker;
        li.addEventListener("click", () => selectCompany(company));
        list.appendChild(li);
    });

    if (companies.length > 0) {
        selectCompany(companies[0]);
    }
});

function selectCompany(company) {
    console.log(company);
    document.getElementById("selected-company").textContent =
    `${company.name} (${company.ticker})`;

    const statusMsg = document.getElementById("status-message");
    const chartContainer = document.getElementById("stockChart");

    chartContainer.style.display = "none";
    statusMsg.style.display = "block";
    const startTime = Date.now();

    // Fetch chart prices
    fetch(`/prices?ticker=${company.ticker}&period=3mo&interval=1d`)
        .then(res => res.json())
        .then(data => {
        if (data.length === 0) {
            statusMsg.textContent = "⚠ No data available.";
            return;
        }

        const dates = data.map(d => d.date);
        const prices = data.map(d => d.close);

        const elapsed = Date.now() - startTime;
        const wait = Math.max(0, 1200 - elapsed);

        setTimeout(() => {
            statusMsg.style.display = "none";
            chartContainer.style.display = "block";
            renderChart(dates, prices, company.ticker);

            //  fetch indicators only AFTER chart exists
            fetchIndicators(company.ticker);
        }, wait);
    })
        .catch(err => console.error(err));

    //. Fetch company stats
    fetch(`/stats?ticker=${company.ticker}`)
        .then(res => res.json())
        .then(stats => {
        document.getElementById("stat-high").textContent =
        `52-Week High: $${stats.high_52week}`;
        document.getElementById("stat-low").textContent =
        `52-Week Low: $${stats.low_52week}`;
        document.getElementById("stat-volume").textContent =
        `Average Volume: ${stats.avg_volume.toLocaleString()}`;
    })
        .catch(err => console.error("Stats fetch failed:", err));
}

// Fetch indicators and add to chart
function fetchIndicators(ticker) {
    fetch(`/indicators?ticker=${ticker}`)
        .then(res => res.json())
        .then(indicators => {
        if (!indicators || indicators.length === 0) return;

        const dates = indicators.map(d => d.date);
        const sma = indicators.map(d => d.SMA_20);
        const ema = indicators.map(d => d.EMA_20);

        // Update labels
        stockChart.data.labels = dates;

        // Remove old SMA/EMA if reloading
        stockChart.data.datasets = stockChart.data.datasets.filter(
            ds => !["SMA (20)", "EMA (20)"].includes(ds.label)
        );

        // SMA (orange dashed)
        stockChart.data.datasets.push({
            label: "SMA (20)",
            data: sma,
            borderColor: "orange",
            borderDash: [5, 5],
            fill: false,
            tension: 0.1
        });

        stockChart.data.datasets.push({
            label: "EMA (20)",
            data: ema,
            borderColor: "green",
            fill: false,
            tension: 0.1
        });

        stockChart.update();

        const latestRSI = indicators.map(d => d.RSI).filter(v => v !== null).pop();
        if (latestRSI) {
            document.getElementById("stat-rsi").textContent =
            `RSI (14): ${latestRSI.toFixed(2)}`;
        }
    })
        .catch(err => console.error("Indicators fetch failed:", err));
}

function renderChart(labels, data, ticker) {
    const ctx = document.getElementById("stockChart").getContext("2d");
    if (stockChart) {
        stockChart.destroy();
    }
    stockChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: `${ticker} Stock Price`,
                data: data,
                borderColor: "blue",
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: { title: { display: true, text: "Closing Price" } }
            }
        }
    });
}
