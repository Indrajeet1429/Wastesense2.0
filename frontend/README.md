# WasteSense frontend (React + Vite)

Monitoring and intelligence UI for WasteSense. React 18, React Router 6, Vite. No chart or UI libraries.

## Run
Create an account on the sign in screen, then explore the app.
```bash
cd frontend
npm install
cp .env.example .env     # VITE_USE_MOCK=true uses sample data
npm run dev              # http://localhost:5173
npm run build            # production build in dist/
```

## Structure
```
src/
  main.jsx, App.jsx            entry and routes only
  pages/                       one file per screen
    Dashboard, Machines, MachineDetails, Trends        Member 3 (monitoring)
    WasteEvents, WasteDetails, Replay, Optimization, Savings   Member 4 (intelligence)
    Alerts                     listed under both members in the brief: agree one owner
    Landing, Login, NotFound   shared
  components/
    common/   Logo, Icon, Badge, Panel, PageHeader, Note, DataState, AppLayout, ProtectedRoute
    cards/    StatCard, CaseSection, Fingerprint, BigNumbers
    charts/   LineChart, BarChart, ExpectedActual, Meter, ChartLegend
    tables/   DataTable
    alerts/   AlertSummary, AlertTable
  hooks/      useApi, useAuth, useTheme
  services/   api.js (HTTP client), wastesenseService.js (all data calls), mockData.js, authService.js
  styles/     global.css (tokens), landing.css, app.css
  utils/      format.js, constants.js
```

## Connect FastAPI
1. In `.env` set `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=/api/v1`. The dev server proxies `/api` to `http://localhost:8000`
   (change with `VITE_PROXY_TARGET`).
2. Responses must match the agreed `docs/interfaces.md`. A draft is in `docs/interfaces.draft.md`; reconcile the two.
3. Pages only import from `services/wastesenseService.js`, so no page code changes are needed.
4. Replace `login` and `register` in `services/authService.js` with calls to your auth endpoints, then call `setToken(token)`.

## Rules the UI follows
- No waste intelligence is calculated in the frontend. Scores, excess values, confidence and savings come from the API.
- Replay is labelled "Model-based counterfactual estimate"; savings are "Estimated potential savings".
- Mock data is labelled with a "Sample data" badge and lives only in `services/mockData.js`.

## Git
Work on your own branch (`member3-monitoring-ui` or `member4-intelligence-ui`), never commit to `main`, push only your branch and merge
through a Pull Request. Change shared files (`components/`, `styles/`, `utils/`, `App.jsx`) only after coordinating.
