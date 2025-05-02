import { getSession } from "./session.js";

window.onload = () => {
    const { accountType, accountId } = getSession();

    if (accountType !== "business" || !accountId) {
        window.location.href = "/";
        return;
    }

    const path = window.location.pathname;

    if (path.endsWith("/manage")) {
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
    } else if (path.endsWith("/create")) {
        const form = document.getElementById("createBusinessForm");
        form.onsubmit = async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const body = {
                account_id: accountId,
                name: formData.get("name"),
                address: formData.get("address"),
                city: formData.get("city"),
                state: formData.get("state"),
                postal_code: formData.get("postal_code"),
                latitude: parseFloat(formData.get("latitude")),
                longitude: parseFloat(formData.get("longitude")),
                is_open: formData.get("is_open") === "true",
                attributes: JSON.parse(formData.get("attributes")),
                categories: formData.get("categories").split(",").map(x => x.trim()),
                hours: JSON.parse(formData.get("hours"))
            };

            try {
                const res = await fetch("/api/business/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(body)
                });

                const data = await res.json();
                if (data.success) {
                    alert("Business created!");
                    window.location.href = "/manage";
                } else {
                    alert("Failed to create business: " + data.error);
                }
            } catch (err) {
                alert("Internal error.");
                console.error(err);
            }
        };
    }
};
