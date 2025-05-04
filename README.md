🧠 SHL Test Recommendation System
A full-stack project that scrapes SHL's product catalog using Selenium, builds a TF-IDF-based recommendation engine, and serves results via a Flask backend connected to a React frontend.

📌 Overview
This system recommends SHL assessment tests based on user-entered queries using natural language similarity.

🔧 Tech Stack
Scraping: Python, Selenium, WebDriver

Data Management: pandas

Recommendation Engine: scikit-learn (TF-IDF Vectorizer + Cosine Similarity)

Backend: Flask (served on port 8080 locally)

Frontend: React

Deployment: Hosted on Render (backend), deployable on Vercel (frontend)

🗂️ Step 1: Scraping SHL Data
Source URL:
🔗 https://www.shl.com/solutions/products/product-catalog/

Using Selenium and WebDriver, the site was programmatically visited, and relevant test data was extracted, including:

Test name

Description

Category

Direct link to the test page

This data was stored and managed using pandas in a structured format (CSV/JSON).

🤖 Step 2: Recommendation Engine
We built a similarity-based recommendation system that:

Converts test descriptions into vectors using TF-IDF Vectorizer

Compares the user query against all test vectors using Cosine Similarity

Returns the Top 3 closest matches with metadata and similarity score

Libraries Used:
scikit-learn

pandas

numpy

🔌 Step 3: Flask Backend
The backend provides two routes:

/recommend?query=your+input
→ Returns top 3 recommended tests

/search?query=your+input
→ Returns all tests where the query appears in the test name

CORS is enabled to support frontend interaction.

🔁 Example API Call:
bash
Copy
Edit
curl "http://localhost:8080/recommend?query=mid%20level"
Or use the hosted version:

bash
Copy
Edit
curl "https://shl-assignemnt-backend.onrender.com/recommend?query=mid%20level"
🌐 Step 4: React Frontend
A React-based UI allows users to:

Type a query into a search bar

View a list of top 3 recommended SHL tests

See test names, descriptions, links, and similarity scores

Axios is used to connect to the Flask backend:

js
Copy
Edit
axios.get("https://shl-assignemnt-backend.onrender.com/recommend", {
  params: { query: userInput }
});
🚀 Deployment
🔧 Backend (Flask)
Run locally on port 8080

Hosted on Render at:
👉 https://shl-assignemnt-backend.onrender.com

🌐 Frontend (React)
To deploy:

Build the frontend:

bash
Copy
Edit
npm run build
Deploy build/ to:


💡 Example Query
text
Copy
Edit
Query: "mid level"
Result:

Numerical Reasoning Test

Verbal Critical Thinking Test

Deductive Logic Assessment

Each result includes:

Test name

Description

Similarity score

Direct SHL URL


