const API_BASE = "";

let allExpenses = [];


// --------------------------------------------------
// DOM Elements
// --------------------------------------------------

const totalSpending = document.getElementById("totalSpending");
const monthlySpending = document.getElementById("monthlySpending");
const transactionCount = document.getElementById("transactionCount");

const categoryList = document.getElementById("categoryList");
const recentExpenses = document.getElementById("recentExpenses");

const expensesTableBody = document.getElementById("expensesTableBody");
const tableEmptyState = document.getElementById("tableEmptyState");

const categoryFilter = document.getElementById("categoryFilter");

const expenseModal = document.getElementById("expenseModal");
const openExpenseModal = document.getElementById("openExpenseModal");
const closeExpenseModal = document.getElementById("closeExpenseModal");

const expenseForm = document.getElementById("expenseForm");

const formError = document.getElementById("formError");

const toast = document.getElementById("toast");
const toastMessage = document.getElementById("toastMessage");


// --------------------------------------------------
// Utilities
// --------------------------------------------------

function formatCurrency(amount) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2
    }).format(amount);
}


function formatDate(dateString) {
    const date = new Date(`${dateString}T00:00:00`);

    return date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;

    return div.innerHTML;
}


function getInitial(title) {
    return title
        .trim()
        .charAt(0)
        .toUpperCase();
}


function showToast(message) {
    toastMessage.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}


// --------------------------------------------------
// Load Dashboard
// --------------------------------------------------

async function loadDashboard() {

    try {

        const [
            expensesResponse,
            summaryResponse
        ] = await Promise.all([
            fetch(`${API_BASE}/expenses`),
            fetch(`${API_BASE}/expenses/summary`)
        ]);


        if (!expensesResponse.ok || !summaryResponse.ok) {
            throw new Error("Failed to load dashboard data.");
        }


        allExpenses = await expensesResponse.json();

        const summary = await summaryResponse.json();


        updateStats(summary);

        renderCategories(summary.by_category);

        renderRecentExpenses(allExpenses);

        renderExpensesTable(allExpenses);

        populateCategoryFilter(allExpenses);

    } catch (error) {

        console.error(error);

        showToast("Unable to load expense data.");

    }

}


// --------------------------------------------------
// Statistics
// --------------------------------------------------

async function updateStats(summary) {

    totalSpending.textContent =
        formatCurrency(summary.total);


    transactionCount.textContent =
        allExpenses.length;


    const now = new Date();

    const year = now.getFullYear();

    const month = now.getMonth() + 1;


    try {

        const response = await fetch(
            `${API_BASE}/expenses/summary/monthly?year=${year}&month=${month}`
        );


        if (!response.ok) {
            throw new Error("Monthly summary unavailable.");
        }


        const monthly = await response.json();


        monthlySpending.textContent =
            formatCurrency(monthly.total);


        const monthName = now.toLocaleDateString(
            "en-IN",
            { month: "long" }
        );


        document.getElementById("monthlyLabel").textContent =
            monthName;

    } catch (error) {

        monthlySpending.textContent =
            formatCurrency(0);

    }

}


// --------------------------------------------------
// Category Breakdown
// --------------------------------------------------

function renderCategories(categories) {

    categoryList.innerHTML = "";


    const entries = Object.entries(categories);


    if (entries.length === 0) {

        categoryList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">◌</div>
                <p>No spending data yet.</p>
            </div>
        `;

        return;
    }


    const maxAmount = Math.max(
        ...entries.map(([_, amount]) => amount)
    );


    entries
        .sort((a, b) => b[1] - a[1])
        .forEach(([category, amount]) => {

            const percentage =
                maxAmount > 0
                    ? (amount / maxAmount) * 100
                    : 0;


            const row = document.createElement("div");

            row.className = "category-row";


            row.innerHTML = `
                <div class="category-name">
                    ${escapeHtml(category)}
                </div>

                <div class="category-bar">
                    <div
                        class="category-bar-fill"
                        style="width: ${percentage}%"
                    ></div>
                </div>

                <div class="category-amount">
                    ${formatCurrency(amount)}
                </div>
            `;


            categoryList.appendChild(row);

        });

}


// --------------------------------------------------
// Recent Expenses
// --------------------------------------------------

function renderRecentExpenses(expenses) {

    recentExpenses.innerHTML = "";


    if (expenses.length === 0) {

        recentExpenses.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">◌</div>
                <p>No expenses recorded yet.</p>
            </div>
        `;

        return;
    }


    const recent = [...expenses]
        .sort((a, b) => {

            return new Date(b.date) - new Date(a.date);

        })
        .slice(0, 5);


    recent.forEach(expense => {

        const item = document.createElement("div");

        item.className = "recent-item";


        item.innerHTML = `
            <div class="expense-info">

                <div class="expense-avatar">
                    ${escapeHtml(getInitial(expense.title))}
                </div>

                <div>
                    <div class="expense-title">
                        ${escapeHtml(expense.title)}
                    </div>

                    <div class="expense-category">
                        ${escapeHtml(expense.category)}
                        ·
                        ${formatDate(expense.date)}
                    </div>
                </div>

            </div>

            <div class="expense-amount">
                ${formatCurrency(expense.amount)}
            </div>
        `;


        recentExpenses.appendChild(item);

    });

}


// --------------------------------------------------
// Expense Table
// --------------------------------------------------

function renderExpensesTable(expenses) {

    expensesTableBody.innerHTML = "";


    if (expenses.length === 0) {

        tableEmptyState.style.display = "block";

        return;

    }


    tableEmptyState.style.display = "none";


    const sorted = [...expenses]
        .sort((a, b) => new Date(b.date) - new Date(a.date));


    sorted.forEach(expense => {

        const row = document.createElement("tr");


        row.innerHTML = `
            <td>
                ${formatDate(expense.date)}
            </td>

            <td>
                <strong>
                    ${escapeHtml(expense.title)}
                </strong>
            </td>

            <td>
                <span class="category-badge">
                    ${escapeHtml(expense.category)}
                </span>
            </td>

            <td class="amount-cell">
                ${formatCurrency(expense.amount)}
            </td>

            <td>

                <button
                    class="delete-btn"
                    title="Delete expense"
                    data-id="${expense.id}"
                >
                    ×
                </button>

            </td>
        `;


        expensesTableBody.appendChild(row);

    });

}


// --------------------------------------------------
// Category Filter
// --------------------------------------------------

function populateCategoryFilter(expenses) {

    const currentValue = categoryFilter.value;


    const categories = [
        ...new Set(
            expenses.map(expense => expense.category)
        )
    ].sort();


    categoryFilter.innerHTML = `
        <option value="">
            All categories
        </option>
    `;


    categories.forEach(category => {

        const option = document.createElement("option");

        option.value = category;

        option.textContent = category;

        categoryFilter.appendChild(option);

    });


    categoryFilter.value = currentValue;

}


// --------------------------------------------------
// Filter
// --------------------------------------------------

categoryFilter.addEventListener(
    "change",
    async () => {

        const category = categoryFilter.value;


        if (!category) {

            renderExpensesTable(allExpenses);

            return;

        }


        try {

            const response = await fetch(
                `${API_BASE}/expenses?category=${encodeURIComponent(category)}`
            );


            if (!response.ok) {
                throw new Error("Filtering failed.");
            }


            const filtered = await response.json();

            renderExpensesTable(filtered);

        } catch (error) {

            console.error(error);

            showToast("Unable to filter expenses.");

        }

    }
);


// --------------------------------------------------
// Add Expense Modal
// --------------------------------------------------

openExpenseModal.addEventListener(
    "click",
    () => {

        expenseModal.classList.add("active");

        document.getElementById("date").value =
            new Date().toISOString().split("T")[0];

        document.getElementById("title").focus();

    }
);


closeExpenseModal.addEventListener(
    "click",
    closeModal
);


expenseModal.addEventListener(
    "click",
    (event) => {

        if (event.target === expenseModal) {
            closeModal();
        }

    }
);


function closeModal() {

    expenseModal.classList.remove("active");

    expenseForm.reset();

    formError.style.display = "none";

}


// --------------------------------------------------
// Submit Expense
// --------------------------------------------------

expenseForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        formError.style.display = "none";


        const expense = {

            title:
                document.getElementById("title").value.trim(),

            amount:
                Number(document.getElementById("amount").value),

            category:
                document.getElementById("category").value,

            date:
                document.getElementById("date").value

        };


        if (!expense.title) {

            showFormError(
                "Please enter an expense title."
            );

            return;

        }


        if (!expense.amount || expense.amount <= 0) {

            showFormError(
                "Amount must be greater than zero."
            );

            return;

        }


        if (!expense.category) {

            showFormError(
                "Please select a category."
            );

            return;

        }


        try {

            const response = await fetch(
                `${API_BASE}/expenses`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(expense)
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail?.[0]?.msg ||
                    "Unable to add expense."
                );

            }


            closeModal();

            showToast("Expense added successfully.");

            await loadDashboard();

        } catch (error) {

            console.error(error);

            showFormError(error.message);

        }

    }
);


function showFormError(message) {

    formError.textContent = message;

    formError.style.display = "block";

}


// --------------------------------------------------
// Delete Expense
// --------------------------------------------------

expensesTableBody.addEventListener(
    "click",
    async (event) => {

        const button =
            event.target.closest(".delete-btn");


        if (!button) {
            return;
        }


        const expenseId =
            button.dataset.id;


        const confirmed = confirm(
            "Delete this expense?"
        );


        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `${API_BASE}/expenses/${expenseId}`,
                {
                    method: "DELETE"
                }
            );


            if (!response.ok) {
                throw new Error("Unable to delete expense.");
            }


            showToast("Expense deleted.");

            await loadDashboard();

        } catch (error) {

            console.error(error);

            showToast(
                "Unable to delete expense."
            );

        }

    }
);


// --------------------------------------------------
// View All
// --------------------------------------------------

document.getElementById("viewAllBtn")
    .addEventListener(
        "click",
        () => {

            document
                .querySelector(".expenses-panel")
                .scrollIntoView({
                    behavior: "smooth"
                });

        }
    );


// --------------------------------------------------
// Initial Load
// --------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);