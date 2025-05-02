import { getSession } from "./session.js";

window.onload = () => {
    const { accountType, accountId } = getSession();

    if (accountType !== "business" || !accountId) {
        window.location.href = "/";
        return;
    }

    fetch(`/api/businesses?accountId=${accountId}`)
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                alert("Failed to fetch businesses.");
                return;
            }

            const container = document.getElementById("businessList");
            container.innerHTML = "";

            data.businesses.forEach(biz => {
                const bizRow = document.createElement("div");
                bizRow.style.display = "flex";
                bizRow.style.justifyContent = "space-between";
                bizRow.style.borderBottom = "1px solid #eee";
                bizRow.style.padding = "10px";

                const text = document.createElement("span");
                text.innerText = `${biz.name} — ${biz.address} — Rating: ${biz.stars} — Open: ${biz.is_open ? "Yes" : "No"}`;

                const viewBtn = document.createElement("button");
                viewBtn.innerText = "View Details";
                viewBtn.onclick = () => {
                    window.location.href = `/manage/details?businessId=${biz.business_id}`;
                };

                bizRow.appendChild(text);
                bizRow.appendChild(viewBtn);
                container.appendChild(bizRow);
            });
        })
        .catch(err => {
            console.error("Error loading businesses:", err);
            alert("Internal error loading businesses.");
        });
};
