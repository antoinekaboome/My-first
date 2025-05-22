import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [lowStock, setLowStock] = useState([] as any[]);

  useEffect(() => {
    axios.get('/api/products').then((res) => {
      setLowStock(res.data.filter((p: any) => p.quantity <= p.threshold));
    });
  }, []);

  return (
    <div>
      <h2>Low Stock</h2>
      <ul>
        {lowStock.map((p) => (
          <li key={p._id}>{p.name}: {p.quantity}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
