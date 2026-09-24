# API Monitoring & Performance Analysis Dashboard

A web-based dashboard to monitor multiple APIs, check their availability, measure response times, and analyze performance history.

## Features

- **Dashboard** — Overview of total, healthy, slow, and failed APIs with response time charts
- **API Management** — Add, view, and delete APIs with name, URL, and HTTP method
- **Live Monitoring** — Check individual or all APIs with real-time health classification
- **History** — Filterable log of all past monitoring checks
- **Analytics** — Performance charts (response time, success/fail ratio, API comparison)
- **Dark/Light Mode** — Toggle between themes with saved preference

## Health Classification

| Status | Condition |
|---------|-----------|
| Healthy | Response time < 500 ms |
| Slow | Response time 500–2000 ms |
| Failed | Request failure or error response |

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** PHP (upcoming)
- **Database:** MySQL (upcoming)
- **Charts:** Chart.js

## Setup

1. Clone the repo
2. Open `index.html` in a browser (frontend only for now)
3. PHP/MySQL backend will be added in later phases

## Project Structure

```
├── index.html          # Main page
├── css/
│   └── style.css       # Styling (light/dark mode)
├── js/
│   └── app.js          # Frontend logic & mock data
├── .gitignore
└── README.md
```

## License

This project is for academic/educational purposes.
