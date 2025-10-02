# 🚀 React Frontend Basics

## 📘 What is React?

React is a JavaScript library developed by Facebook (now Meta) for building user interfaces. It allows developers to create reusable UI components and manage application state efficiently. React is especially useful for building single-page applications (SPAs) where performance and dynamic content are key.

### 🔧 How React Works

React operates on several key concepts:

**1. Virtual DOM** - React creates a virtual UI representation in memory, compares it with the real DOM when data changes, and only updates what's different (called "reconciliation"). This makes React extremely fast.

**2. Components** - Reusable UI pieces that can be functional (with hooks) or class-based. Each manages its own state, receives data via props, and can contain other components in a tree structure.

**3. JSX** - HTML-like syntax in JavaScript that gets compiled to regular JavaScript. Makes code more readable and easier to write.

**4. Unidirectional Data Flow** - Data flows down from parent to child components via props. State changes trigger re-renders, making behavior predictable and easier to debug.

**5. React Hooks** - Modern approach that allows functional components to use state and other React features. Common hooks: `useState`, `useEffect`, `useContext`.

---

## ⚙️ 1. Set Up Your Environment

Before you start coding, make sure your environment is ready:

- **Install Node.js and npm**: These are required to run React and manage dependencies.
- **Use a code editor**: Visual Studio Code is highly recommended.

To create a new React app, run:

```bash
npx create-react-app my-app
cd my-app
npm start
````
This will launch a development server and open your app in the browser.

## 🧱 2. Understand the File Structure

React apps created with create-react-app have a default structure:

•  public/: Contains static files like index.html.
•  src/: Contains your React components and logic.
  ⁠◦  App.js: The main component of your app.
  ⁠◦  index.js: The entry point that renders the app to the DOM.

### 📁 Adding Pages and Routing

For multi-page applications, you'll need to add routing:

**Install React Router:**
```bash
npm install react-router-dom
```

**Typical structure for pages:**
```
src/
├── components/     # Reusable UI components
├── pages/         # Page components (Home, About, Contact, etc.)
├── services/      # API calls and external services
├── utils/         # Helper functions
├── App.js         # Main app with routing
└── index.js       # Entry point
```

**Example routing setup:**
```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 🔗 Creating API Endpoints (Frontend)

React is frontend-only, but you can make API calls to external services:

**Using Fetch API:**
```javascript
// In src/services/api.js
export const fetchData = async () => {
  const response = await fetch('https://api.example.com/data');
  return response.json();
};
```

**Using Axios (install with `npm install axios`):**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com'
});

export const getData = () => api.get('/data');
export const postData = (data) => api.post('/data', data);
```

This structure helps organize your code, pages, and API integrations efficiently.

## 🚀 3. Build and Deploy

To prepare your app for production:
```bash
    npm run build
```