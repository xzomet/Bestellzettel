let currentTableId = null;
let currentOrderId = null;
let currentBill = 0;
let menuItems = [];
let menuById = {};

let currentDomain = "all"; // all | food | drinks
let currentCategory = "all";

const DOMAIN_CATEGORIES = {
    food: [
        "vorspeisen",
        "suppen",
        "salad",
        "haupt",
        "baguette",
        "beilagen",
        "deserts",
    ],
    drinks: [
        "bier",
        "wein",
        "raki",
        "spirits",
        "non_alcoholic",
        "drinks", // fallback
    ],
};

// ---------- VIEWS ----------

function showView(viewName) {
    document.getElementById("tables_view").style.display = viewName === "tables"
        ? "block"
        : "none";

    document.getElementById("table_view").style.display = viewName === "table"
        ? "block"
        : "none";
}

// ---------- TABLES ----------

async function loadTables() {
    const response = await fetch("/tables");
    const data = await response.json();

    showView("tables");

    const tablesDiv = document.getElementById("tables");
    tablesDiv.innerHTML = "";

    data.tables.forEach((table) => {
        const btn = document.createElement("button");
        btn.textContent = table.name;

        btn.onclick = () => loadTable(table.id);

        tablesDiv.appendChild(btn);
    });
}

// ---------- TABLE VIEW ----------

async function loadTable(table_id) {
    console.log("loadTable() called");
    const response = await fetch(`/tables/${table_id}`);
    const data = await response.json();

    console.log("TOTAL FROM BACKEND:", data.total_price_cents);
    currentTableId = data.table_id;
    currentOrderId = data.order_id;
    currentBill = data.total_price_cents;

    showView("table");

    document.getElementById("table_title").textContent =
        `Table ${currentTableId}`;

    // ---- total ----
    document.getElementById("order_total").textContent = `Total: €${
        (data.total_price_cents / 100).toFixed(2)
    }`;

    const orderDiv = document.getElementById("order_items");
    orderDiv.innerHTML = "";

    data.order_items.forEach((item) => {
        const row = document.createElement("div");

        const minusBtn = document.createElement("button");
        minusBtn.textContent = "−";
        minusBtn.onclick = () => updateItem(item.menu_item_id, -1);

        const plusBtn = document.createElement("button");
        plusBtn.textContent = "+";
        plusBtn.onclick = () => updateItem(item.menu_item_id, +1);

        const menuItem = menuById[item.menu_item_id];
        const label = document.createElement("span");
        label.textContent = ` ${menuItem.name} x${item.quantity} (€${
            (menuItem.price_cents / 100).toFixed(2)
        }) `;

        row.appendChild(minusBtn);
        row.appendChild(label);
        row.appendChild(plusBtn);

        orderDiv.appendChild(row);
    });
}

// ---------- MENU ----------

async function loadMenu() {
    console.log("loadMenu() called");
    const response = await fetch("/menu");
    const data = await response.json();

    console.log("menu data:", data);

    menuItems = data.menu;
    menuById = {};

    menuItems.forEach((item) => {
        menuById[item.id] = item;
    });

    renderDomains();
    renderCategories();
    renderMenu();
}

function renderDomains() {
    const div = document.getElementById("menu_domains");
    div.innerHTML = "";

    ["all", "food", "drinks"].forEach((domain) => {
        const btn = document.createElement("button");
        btn.textContent = domain.toUpperCase();

        btn.onclick = () => {
            currentDomain = domain;
            currentCategory = "all";
            renderCategories();
            renderMenu();
        };

        div.appendChild(btn);
    });
}

function renderCategories() {
    const div = document.getElementById("menu_categories");
    div.innerHTML = "";

    if (currentDomain === "all") return;

    const allowed = DOMAIN_CATEGORIES[currentDomain] || [];

    const categories = ["all"];
    menuItems.forEach((item) => {
        const cat = item.category ?? "other";
        if (allowed.includes(cat) && !categories.includes(cat)) {
            categories.push(cat);
        }
    });

    categories.forEach((cat) => {
        const btn = document.createElement("button");
        btn.textContent = cat.toUpperCase();

        btn.onclick = () => {
            currentCategory = cat;
            renderMenu();
        };

        div.appendChild(btn);
    });
}

function renderMenu() {
    const menuDiv = document.getElementById("menu");
    menuDiv.innerHTML = "";

    menuItems
        .filter((item) => {
            const cat = item.category ?? "other";

            if (currentDomain !== "all") {
                const allowed = DOMAIN_CATEGORIES[currentDomain] || [];
                if (!allowed.includes(cat)) return false;
            }

            if (currentCategory !== "all") {
                return cat === currentCategory;
            }

            return true;
        })
        .forEach((item) => {
            const btn = document.createElement("button");
            btn.textContent = `${item.name} (€${
                (item.price_cents / 100).toFixed(2)
            })`;
            btn.onclick = () => addItem(item.id);
            menuDiv.appendChild(btn);
        });
}
// ---------- MUTATIONS ----------

async function addItem(menuItemId) {
    const response = await fetch(
        `/orders/items?table_id=${currentTableId}&menu_item_id=${menuItemId}&delta=1`,
        { method: "POST" },
    );
    const result = await response.json();
    currentOrderId = result.order_id;

    await loadTable(currentTableId);
}

async function updateItem(menuItemId, delta) {
    const response = await fetch(
        `/orders/items?table_id=${currentTableId}&menu_item_id=${menuItemId}&delta=${delta}&order_id=${currentOrderId}`,
        { method: "POST" },
    );

    const result = await response.json();
    currentOrderId = result.order_id;

    await loadTable(currentTableId);
}

async function closeOrder() {
    if (!currentOrderId) await loadTables();

    if (currentBill > 0) {
        const ok = confirm("Has the customer paid?");
        if (!ok) return;
    }

    await fetch(
        `/orders/${currentOrderId}/close`,
        { method: "POST" },
    );

    currentTableId = null;
    currentOrderId = null;

    await loadTables();
}

// ---------- INIT ----------
//

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("close_order").onclick = () => {
        closeOrder();
    };

    document.getElementById("back_btn").onclick = () => {
        currentTableId = null;
        currentOrderId = null;
        showView("tables");
    };

    loadMenu();
    loadTables();
});
