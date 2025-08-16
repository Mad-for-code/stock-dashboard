fetch("/companies")
  .then(res => res.json())
  .then(companies => {
    const list = document.getElementById("company-list");
    companies.forEach(company => {
        const li = document.createElement("li");
        li.textContent = company.name;
        li.dataset.ticker = company.ticker
        li.addEventListener("click", () => selectCompany(company));
        list.appendChild(li);
    })
})
function selectCompany(company) {
    console.log(company);
    document.getElementById("selected-company").textContent = `${company.name} (${company.ticker})`;
}