// Member 4 (intelligence): Detection, Evidence, Root cause, Replay, Savings, Recommendation
import { Link, useParams } from "react-router-dom";
import PageHeader from "../components/common/PageHeader";
import Panel from "../components/common/Panel";
import DataState from "../components/common/DataState";
import CaseSection from "../components/cards/CaseSection";
import Fingerprint from "../components/cards/Fingerprint";
import BigNumbers from "../components/cards/BigNumbers";
import ExpectedActual from "../components/charts/ExpectedActual";
import DataTable from "../components/tables/DataTable";
import Note from "../components/common/Note";
import useApi from "../hooks/useApi";
import { getWasteEvent } from "../services/wastesenseService";
import { formatDateTime } from "../utils/format";

export default function WasteDetails() {
  const { id } = useParams();
  const state = useApi(() => getWasteEvent(id), [id]);
  return (
    <DataState state={state}>{(e) => (
      <>
        <PageHeader title={`${e.waste_id} on ${e.machine_id}`} question={formatDateTime(e.timestamp)}>
          <Link className="btn sm" to="/waste-events">All events</Link>
          <Link className="btn sm" to={`/replay/${e.waste_id}`}>Open replay</Link>
        </PageHeader>
        <Panel className="file">
          <CaseSection n={1} title="Detection"><Fingerprint event={e} /></CaseSection>
          <CaseSection n={2} title="Evidence">
            <ExpectedActual rows={[
              { label: "CPU", actual: e.actual_cpu, expected: e.expected_cpu, unit: "%" },
              { label: "Memory", actual: e.actual_memory, expected: e.expected_memory, unit: "%" },
              { label: "Power", actual: e.actual_power, expected: e.expected_power, unit: " W" },
            ]} />
            <DataTable rows={[
              { r: "CPU", a: `${e.actual_cpu}%`, x: `${e.expected_cpu}%`, d: `${e.cpu_excess}%` },
              { r: "Memory", a: `${e.actual_memory}%`, x: `${e.expected_memory}%`, d: `${e.memory_excess}%` },
              { r: "Power", a: `${e.actual_power} W`, x: `${e.expected_power} W`, d: `${e.power_excess} W` },
            ]} rowKey="r" columns={[
              { header: "Resource", cell: (r) => r.r }, { header: "Actual", cell: (r) => r.a },
              { header: "Expected", cell: (r) => r.x }, { header: "Excess", cell: (r) => r.d },
            ]} />
          </CaseSection>
          <CaseSection n={3} title="Root cause">
            <p className="sub">Likely contributing factors</p>
            <ol className="cf">{e.contributing_factors.map((f) => <li key={f}>{f}</li>)}</ol>
            <p className="sub" style={{ marginTop: 12 }}>These factors come from the model. They do not prove causality.</p>
          </CaseSection>
          <CaseSection n={4} title="Replay">
            <Note style={{ marginBottom: 12 }}>Model-based counterfactual estimate. Not measured real-world savings.</Note>
            <BigNumbers items={[
              { label: "Current", value: [`${e.actual_cpu}% CPU`, `${e.actual_power} W`] },
              { label: "Replay", value: [`${e.expected_cpu}% CPU`, `${e.expected_power} W`] },
              { label: "Potential difference", value: `${e.power_excess} W` },
            ]} />
          </CaseSection>
          <CaseSection n={5} title="Savings">
            <BigNumbers items={[
              { label: "CPU cores", value: e.savings.cpu_cores }, { label: "Memory", value: `${e.savings.memory_gb} GB` }, { label: "Power", value: `${e.savings.power_w} W` },
            ]} />
            <p className="sub" style={{ marginTop: 10 }}>Estimated potential savings: about ${e.savings.cost_usd_month} per month. Not guaranteed.</p>
          </CaseSection>
          <CaseSection n={6} title="Recommendation">
            <p style={{ marginTop: 0 }}>Review the allocation on {e.machine_id} and reduce reserved capacity toward the expected level. Check the waste score again after one full workload cycle.</p>
            <Link className="btn sm" to="/optimization">See optimization</Link>
          </CaseSection>
        </Panel>
      </>
    )}</DataState>
  );
}
