# AI Notes

## 1. Overview

This project was developed with the help of AI tools, primarily ChatGPT, as an engineering assistant throughout the development process.

I used AI for understanding the assignment, planning the implementation, debugging issues, improving the UI/UX, reviewing code, writing and improving tests, and preparing documentation.

AI was not treated as an unquestioned source of truth. Suggestions were implemented, tested locally, and modified whenever they did not work correctly with the actual application.

The final implementation was built around the requirements of the assignment while keeping the architecture simple, understandable, and easy to run.

---

## 2. Why I Chose This Architecture

The core requirement of the assignment was to build a REST API for managing personal expenses.

I chose:

- Python
- FastAPI
- Pydantic
- Pytest
- HTML
- CSS
- Vanilla JavaScript
- In-memory storage

The backend follows a relatively simple structure:

```text
Client / Frontend
       |
       v
    FastAPI
       |
       v
   API Routes
       |
       v
 Pydantic Models
       |
       v
 In-Memory Storage
```

The frontend communicates with the backend through HTTP requests.

For example:

```text
Add Expense
    |
    v
POST /expenses
    |
    v
FastAPI validation
    |
    v
Store expense
    |
    v
Return JSON response
    |
    v
Frontend refreshes dashboard
```

I intentionally avoided introducing unnecessary architectural layers because the application is relatively small.

For a production-scale system, a more elaborate service/repository architecture could make sense, but for a four-hour assignment it would add complexity without providing enough value.

---

## 3. AI-Generated vs. Personally Written Code

AI was involved in generating and suggesting parts of the implementation, but the final code was reviewed, integrated, tested, and modified by me.

### AI-assisted areas

AI helped with:

- Initial project structure
- FastAPI route implementation ideas
- Pydantic model structure
- In-memory storage implementation
- Expense summary logic
- Monthly summary logic
- Pytest test case suggestions
- Frontend API integration
- Dashboard rendering logic
- Search and filtering logic
- UI/UX styling suggestions
- Responsive CSS
- Debugging frontend/backend issues
- README and AI documentation structure

### Areas I personally worked through and validated

I personally:

- Set up the project environment
- Created and configured the virtual environment
- Installed dependencies
- Ran the FastAPI server
- Tested endpoints using Swagger
- Tested the frontend in the browser
- Added sample expenses
- Checked actual API responses
- Debugged frontend state/update problems
- Verified search and filtering behavior
- Verified deletion behavior
- Ran the automated test suite
- Investigated failed requests
- Checked UI behavior after changes
- Decided which AI suggestions were appropriate
- Modified code when AI-generated solutions did not match the actual application
- Performed final end-to-end testing

The final implementation should therefore be considered AI-assisted development rather than blindly AI-generated code.

---

## 4. Why I Used FastAPI

I selected FastAPI because it is well suited to building a small REST API quickly while still providing useful engineering features.

The main reasons were:

- Strong request validation through Pydantic
- Automatic OpenAPI documentation
- Interactive Swagger UI
- Simple route definitions
- Good support for JSON APIs
- Easy integration with Python
- Straightforward testing with FastAPI's test client

The automatic Swagger documentation was particularly useful during development because I could test the API independently of the frontend.

Swagger is available at:

`http://127.0.0.1:8000/docs`

---

## 5. Why I Used In-Memory Storage

The assignment explicitly allows data to be stored in memory or a local JSON file and states that a database is not required.

I therefore used an in-memory Python list.

This keeps the project:

- Simple
- Fast to start
- Easy to understand
- Easy to test
- Free from database configuration
- Free from additional infrastructure

The main trade-off is that data is lost when the server restarts.

For this assignment, that behavior is acceptable because persistent storage was not required.

For a production application, I would replace the in-memory layer with a proper database and persistence layer.

---

## 6. Why I Added a Frontend

The assignment primarily focuses on the REST API, and a frontend was not required.

However, I decided to add a lightweight frontend because I wanted to demonstrate the API through an actual user interface.

The frontend demonstrates:

- REST API integration
- Asynchronous JavaScript
- Form handling
- Client-side validation
- Search
- Category filtering
- Dynamic rendering
- Error handling
- Responsive design
- Dashboard updates
- Delete operations

This also makes the project easier to demonstrate during evaluation.

I intentionally kept the frontend lightweight so that it would complement the API instead of becoming the main focus of the project.

---

## 7. Why I Used HTML/CSS/JavaScript Instead of React

I considered using React for the frontend.

I decided not to use it because the frontend requirements are relatively small and the assignment focuses primarily on backend/API development.

Using React would introduce:

- Node.js dependencies
- A separate frontend build process
- Additional project configuration
- More setup instructions
- More dependencies

Plain HTML, CSS, and JavaScript were sufficient for the required functionality.

This also keeps the repository easier for an evaluator to clone and run.

The frontend communicates directly with the FastAPI backend using the Fetch API.

---

## 8. UI/UX Design Decisions

I chose a clean editorial-style dashboard rather than a highly colorful finance dashboard.

The main design choices were:

- Off-white background
- Dark sidebar
- Muted green accent
- White content cards
- Subtle borders
- Soft shadows
- Serif headings
- Clean sans-serif body text
- Spacious layout
- Minimal visual clutter

I intentionally avoided:

- Large gradients
- Neon colors
- Excessive animations
- Glassmorphism
- Overly complicated charts
- Unnecessary visual effects

The goal was to make the application look polished and professional while keeping it practical and easy to understand.

---

## 9. Issues Encountered During Development

The project involved several debugging issues during implementation.

Rather than assuming that the first implementation was correct, I used the actual API responses, browser behavior, and automated tests to identify where problems were occurring.

### 9.1 Issue: Sending Multiple JSON Objects in One Request

While testing the API, I initially tried sending multiple expense objects in a single `POST /expenses` request.

For example:

```json
{
  "title": "Lunch",
  "amount": 250,
  "category": "Food",
  "date": "2026-07-31"
}
{
  "title": "Bus",
  "amount": 50,
  "category": "Transport",
  "date": "2026-07-31"
}
```

The API returned:

```
422 Unprocessable Content
```

with a JSON parsing error containing:

```
Extra data
```

This was not a backend implementation problem.

The endpoint accepts one JSON object per request.

I corrected the testing process by sending each expense through a separate `POST` request.

This was a useful reminder to distinguish between an implementation problem and an incorrectly formatted API request.

---

## 10. Issue: Unexpected Amount Values in the UI

During frontend testing, I noticed that values entered as whole numbers such as:

```
100
200
```

were sometimes displayed unexpectedly, including values such as:

```
199.80
98
```

Instead of immediately changing the calculation logic, I first inspected the actual data returned by the backend.

I checked:

```
GET /expenses
```

and:

```
GET /expenses/summary
```

This allowed me to determine whether the problem was happening during:

- User input
- JavaScript number conversion
- Backend storage
- Summary calculation
- Currency formatting
- UI rendering

The frontend converts the form value using:

```javascript
amount: Number(document.getElementById("amount").value)
```

Currency formatting is handled separately:

```javascript
function formatCurrency(amount) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2
    }).format(amount);
}
```

I kept two decimal places in the currency formatter because expense amounts can legitimately contain decimal values.

The important debugging step was checking the actual API response rather than assuming the display formatter was modifying the stored amount.

---

## 11. Issue: Recent Expenses Were Not Updating

Another issue was that the dashboard statistics updated correctly after adding an expense, but the Recent Expenses section did not update.

The following values were updating:

- Total spending
- This month's spending
- Transaction count
- Spending by category

However, recent expenses remained unchanged.

I traced the frontend data flow:

```text
Add Expense
     |
     v
POST /expenses
     |
     v
Backend stores expense
     |
     v
Reload dashboard
     |
     v
GET /expenses
     |
     v
Update allExpenses
     |
     v
Re-render dashboard
```

After successfully creating an expense, the frontend calls:

```javascript
await loadDashboard();
```

The dashboard then retrieves the latest data from the API.

I made sure that the Recent Expenses section was also rendered using the refreshed `allExpenses` data.

This solved the synchronization problem.

---

## 12. Issue: Transaction Table Was Not Showing Expenses

I also encountered an issue where the Transactions section displayed correctly:

```text
TRANSACTIONS

All expenses
Search expenses...

All categories

Date | Expense | Category | Amount
```

but the transaction rows were not appearing.

The backend was already returning the correct expense data, so I investigated the frontend.

I checked:

- API response
- `allExpenses`
- Table body element
- Rendering function
- Dashboard load order
- JavaScript execution

The table is populated using:

```javascript
renderExpensesTable(allExpenses);
```

I ensured that this function was called after the API response had been loaded into `allExpenses`.

The issue was therefore related to frontend rendering/state synchronization rather than the backend API.

---

## 13. Issue: Category Dropdown Styling

The category filter initially appeared as a default browser `<select>` element.

Functionally it worked, but visually it did not match the rest of the application.

I considered replacing it with a completely custom JavaScript dropdown.

I decided not to do that.

Instead, I kept the native `<select>` and styled it with CSS.

I added:

- Custom border
- Rounded corners
- Custom dropdown arrow
- Matching typography
- Hover state
- Focus state
- Consistent spacing
- Application color scheme

I chose this approach because the native select is simpler and generally more accessible, while CSS was sufficient to make it visually consistent.

One limitation is that the opened option list can still look slightly different depending on the browser and operating system.

For this assignment, I considered that an acceptable trade-off.

---

## 14. Frontend and Backend State Synchronization

One of the important implementation lessons was ensuring that the frontend state reflected the backend state.

The frontend maintains:

```javascript
let allExpenses = [];
```

After adding or deleting an expense, I refresh the dashboard data from the backend rather than manually trying to update every UI component individually.

The flow is:

```text
Backend
   |
   v
GET /expenses
   |
   v
allExpenses
   |
   +------------------+
   |                  |
   v                  v
Recent Expenses    Transactions
   |
   +------------------+
   |
   v
Search / Filter
```

This approach avoids having multiple independent copies of the expense data in the frontend.

---

## 15. Testing Strategy

Testing was an important part of the implementation.

I did not rely only on manually testing the API through Swagger.

The automated test suite covers the main API behavior.

The tests include:

- Creating an expense
- Retrieving expenses
- Filtering by category
- Case-insensitive category filtering
- Calculating overall spending
- Calculating spending by category
- Calculating monthly spending
- Validating invalid amounts
- Validating required fields
- Deleting an expense
- Handling deletion of a non-existent expense

The test suite initially contained 13 tests.

After identifying another behavior that should be covered, I added another test.

The final test result was:

```
14 passed
```

This gave me confidence that changes to the API did not break existing functionality.

---

## 16. Automated Test Result

The final test command was:

```
pytest
```

The result was:

```
============================== test session starts ==============================
collected 14 items

tests\test_expenses.py ..............                                       [100%]

========================= 14 passed, 1 warning ================================
```

There was one dependency-related deprecation warning involving the FastAPI/Starlette test client and HTTPX.

The warning did not cause any test failures.

All 14 tests passed successfully.

---

## 17. How I Validated AI Suggestions

Whenever AI suggested a code change, I did not assume that the suggestion was correct.

My general process was:

1. Understand what the suggested code was doing.
2. Add or modify the code.
3. Start the application.
4. Test the affected functionality.
5. Check the actual API response.
6. Run the automated tests.
7. Check the frontend if the change affected the UI.
8. Keep, modify, or reject the suggestion based on the result.

This was particularly important during frontend debugging.

A code suggestion can look correct in isolation but still fail when it interacts with the actual HTML structure, API response, or existing JavaScript.

---

## 18. AI Suggestions I Decided Not to Use

### 18.1 Database Integration

I considered using SQLite or another database to make the application more realistic.

I decided not to use one.

The assignment explicitly allows in-memory storage and states that a database is not required.

Adding a database would introduce:

- Database configuration
- Schema management
- Additional dependencies
- More setup steps
- Additional testing requirements

For the scope of this assignment, I felt the additional complexity was not justified.

The trade-off is that data is lost when the server restarts, but this is acceptable because the assignment explicitly permits in-memory storage.

### 18.2 React Frontend

I considered using React.

I decided against it because the frontend is relatively small and the assignment focuses primarily on backend/API development.

Using React would introduce:

- Node.js dependencies
- A separate frontend build process
- Additional configuration
- More setup instructions

Plain HTML, CSS, and JavaScript were enough for the requirements.

### 18.3 Persistent JSON Storage

The assignment also allows storing data in a local JSON file.

I considered this approach but decided to use in-memory storage.

JSON persistence would require additional file handling and introduce additional considerations around reading, writing, and maintaining the file.

Since persistence was not required, I preferred the simpler implementation.

### 18.4 Over-Engineered Architecture

I avoided introducing a large controller-service-repository architecture.

For a larger production application, additional layers could be useful.

However, this project has a relatively small scope.

I preferred a structure where the responsibilities are clear without forcing the reviewer to navigate through many unnecessary abstraction layers.

The goal was to use an architecture appropriate for the size of the problem rather than adding complexity simply to make the project appear more sophisticated.

---

## 19. Security and Reliability Considerations

Even though this is a small assignment, I considered basic security and reliability concerns.

The backend validates incoming data using Pydantic.

For example:

- Title cannot be empty.
- Title has a maximum length.
- Amount must be greater than zero.
- Category cannot be empty.
- Date must be a valid date.

The frontend also performs basic validation so users receive immediate feedback.

However, frontend validation is not treated as the final security boundary.

Backend validation remains the source of truth.

I also added an `escapeHtml()` helper in the frontend before inserting user-provided text into generated HTML.

This prevents expense titles and categories containing HTML from being directly interpreted as markup.

---

## 20. Why I Chose a Monthly Summary Endpoint

The assignment lists monthly summary as an optional bonus feature.

I decided to implement it because it provides useful functionality without significantly increasing the complexity of the project.

The endpoint is:

```
GET /expenses/summary/monthly?year=YYYY&month=MM
```

It returns:

- Year
- Month
- Total monthly spending
- Transaction count
- Spending by category

This endpoint is also used by the frontend dashboard to display the current month's spending.

This allowed the optional functionality to have a practical purpose rather than being added only for the sake of having another endpoint.

---

## 21. Why I Used Swagger/OpenAPI

FastAPI automatically provides OpenAPI documentation.

I used the generated Swagger UI throughout development to test the API independently from the frontend.

The documentation is available at:

`http://127.0.0.1:8000/docs`

This was useful for:

- Testing POST requests
- Checking request validation
- Viewing response structures
- Testing filtering
- Testing summaries
- Testing deletion
- Debugging request formatting

I consider the automatic API documentation one of the useful benefits of choosing FastAPI.

---

## 22. What I Learned During the Project

One of the biggest lessons from this assignment was that building an application is not only about writing the initial code.

Debugging and verification were equally important.

I encountered situations where:

- The API worked but the UI did not update.
- Dashboard statistics updated while individual expense lists did not.
- A JSON request failed because the request format was incorrect.
- A native browser control did not match the application's visual design.
- A displayed amount did not immediately match what I expected.

Instead of changing random parts of the code, I learned to trace the complete data flow.

For example:

```text
User Input
    |
    v
Frontend JavaScript
    |
    v
HTTP Request
    |
    v
FastAPI
    |
    v
Pydantic Validation
    |
    v
Storage
    |
    v
API Response
    |
    v
Frontend State
    |
    v
UI Rendering
```

This approach made it easier to identify where an issue was actually occurring.

---

## 23. Engineering Decisions

Throughout the project, I tried to balance functionality, maintainability, and development time.

Some of the main decisions were:

| Decision | Reason |
|---|---|
| FastAPI | Simple REST API development and automatic OpenAPI docs |
| Pydantic | Strong request validation |
| In-memory storage | Explicitly permitted and keeps setup simple |
| Pytest | Automated regression testing |
| Vanilla JavaScript | Avoid unnecessary frontend build complexity |
| CSS dashboard | Lightweight but polished UI |
| Monthly summary | Useful optional functionality |
| Native select + CSS | Simpler and more accessible than custom JS dropdown |
| Backend refresh after mutations | Keeps frontend state consistent |
| Minimal architecture | Appropriate for the assignment's scope |

---

## 24. Final Verification

Before preparing the submission, I verified the project locally.

**Start the application**

```
uvicorn src.main:app --reload
```

**Open the application**

`http://127.0.0.1:8000`

**Open Swagger documentation**

`http://127.0.0.1:8000/docs`

**Run automated tests**

```
pytest
```

Final test result:

```
14 passed
```

I also manually tested the main user flow:

```text
Open dashboard
      |
      v
Add expense
      |
      v
Verify dashboard statistics
      |
      v
Verify recent expenses
      |
      v
Verify transaction table
      |
      v
Search expense
      |
      v
Filter by category
      |
      v
Delete expense
      |
      v
Verify dashboard updates
```

---

## 25. Final Reflection

AI was useful throughout this project, but I did not use it simply as a tool to generate the entire application.

I used it as a development assistant for:

- Understanding requirements
- Planning
- Implementation suggestions
- Debugging
- Testing
- UI/UX improvements
- Code review
- Documentation

The actual development process involved repeatedly implementing, running, testing, identifying problems, and making decisions about whether an AI suggestion was appropriate.

The final implementation prioritizes:

- Correct REST API behavior
- Clear input validation
- Automated testing
- Simple architecture
- Easy setup
- Automatic API documentation
- A polished but lightweight frontend

I intentionally avoided unnecessary infrastructure such as a database or a frontend framework because they were not required for this assignment.

For the scope of the Smart Expense Tracker, I believe a simple, tested, understandable application is more valuable than an over-engineered solution.

The project also helped me practice an important engineering workflow:

```text
Understand
    ↓
Design
    ↓
Implement
    ↓
Run
    ↓
Test
    ↓
Debug
    ↓
Validate
    ↓
Refine
    ↓
Document
```

That workflow was more important to me than simply getting the API to work once.