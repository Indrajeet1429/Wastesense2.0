// The only file pages use to get data. Mock vs FastAPI is decided here, so pages never change.
import { request, USE_MOCK } from "./api";
import * as mock from "./mockData";

const pick = (path, mockFn) => (USE_MOCK ? Promise.resolve(mockFn()) : request(path));

export const getDashboard = () => pick("/dashboard", mock.dashboard);
export const getMachines = () => pick("/machines", () => mock.MACHINES);
export const getMachine = (id) => pick(`/machines/${id}`, () => mock.machine(id));
export const getTrends = (range) => pick(`/trends?range=${range}`, () => mock.trends(range));
export const getAlerts = () => pick("/alerts", () => mock.ALERTS);
export const getWasteEvents = () => pick("/waste-events", () => mock.EVENTS);
export const getWasteEvent = (id) => pick(`/waste-events/${id}`, () => mock.wasteEvent(id));
export const getOptimization = () => pick("/optimization", () => mock.OPTIMIZATION);
export const getSavings = () => pick("/savings", mock.savings);
