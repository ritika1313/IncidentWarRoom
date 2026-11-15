# War-Room Frontend

React + Vite + Tailwind + Axios dashboard for the FastAPI backend (backend is unchanged).

```bash
# terminal 1 (project root)
uvicorn app.main:app --reload

# terminal 2
cd frontend
npm install
npm run dev        # http://localhost:5173
npm run build      # production build
```

- Requests go to `/api/*`; Vite proxies them to `http://127.0.0.1:8000` (the backend has no CORS middleware).
  Override with `VITE_BACKEND_URL` (proxy target) or `VITE_API_BASE_URL` (direct calls, needs CORS).
- Incident History lists incident IDs created/opened in this browser (localStorage), because the backend has no list endpoint.
