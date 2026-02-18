import { useEffect, useState } from "react";
import axios from "axios";

export default function Stats({ refreshKey }) {
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/tickets/stats/");
      setStats(res.data);
    } catch (err) {
      console.log("Error fetching stats:", err);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [refreshKey]);

  if (!stats) return <p>Loading stats...</p>;

  return (
    <div style={{ padding: "15px", border: "1px solid #ddd", marginBottom: "20px" }}>
      <h2> Ticket Stats</h2>

      <p><b>Total Tickets:</b> {stats.total_tickets}</p>
      <p><b>Open Tickets:</b> {stats.open_tickets}</p>
      <p><b>Avg Tickets/Day:</b> {stats.avg_tickets_per_day}</p>

      <h3>Priority Breakdown</h3>
      <ul>
        {stats.priority_breakdown.map((p, index) => (
          <li key={index}>
            {p.priority} : {p.count}
          </li>
        ))}
      </ul>

      <h3>Category Breakdown</h3>
      <ul>
        {stats.category_breakdown.map((c, index) => (
          <li key={index}>
            {c.category} : {c.count}
          </li>
        ))}
      </ul>
    </div>
  );
}
