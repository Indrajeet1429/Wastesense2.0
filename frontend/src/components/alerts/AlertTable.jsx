import { Link } from "react-router-dom";
import DataTable from "../tables/DataTable";
import Badge from "../common/Badge";
import { formatDateTime } from "../../utils/format";

export default function AlertTable({ alerts }) {
  return (
    <DataTable rowKey="alert_id" rows={alerts} columns={[
      { header: "Machine", cell: (a) => <Link to={`/machines/${a.machine_id}`}><b>{a.machine_id}</b></Link> },
      { header: "Time", cell: (a) => formatDateTime(a.timestamp) },
      { header: "Severity", cell: (a) => <Badge value={a.severity} /> },
      { header: "Message", cell: (a) => a.message },
      { header: "Status", cell: (a) => <Badge value={a.status} /> },
    ]} />
  );
}
