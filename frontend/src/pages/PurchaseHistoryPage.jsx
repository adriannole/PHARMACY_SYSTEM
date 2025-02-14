import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/PurchaseHistoryPage.css";

const PurchaseHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPurchaseHistory = async () => {
      if (!username) {
        setError("No user logged in. Please log in first.");
        return;
      }

      try {
        setIsLoading(true);
        const response = await fetch(`http://localhost:4014/purchase_history/${username}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch purchase history");
        }

        const data = await response.json();
        setHistory(data);
      } catch (error) {
        console.error("Error fetching purchase history:", error);
        setError("Failed to fetch purchase history. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchPurchaseHistory();
  }, [username]);

  if (error) {
    return <div className="error-container"><p>{error}</p></div>;
  }

  return (
    <div className="history-container">
      <h2>{username ? `${username}'s Purchase History` : "Purchase History"}</h2>
      {isLoading ? (
        <p className="loading">Loading...</p>
      ) : history.length === 0 ? (
        <p className="empty-history">No purchase history found.</p>
      ) : (
        <ul className="history-list">
          {history.map((item, index) => (
            <li key={index} className="history-item">
              <span className="item-name">{item.product_name}</span>
              <span className="item-quantity">Quantity: {item.quantity}</span>
              <span className="item-price">Price: ${item.price}</span>
              <span className="item-date">Date: {item.date}</span>
            </li>
          ))}
        </ul>
      )}
      <button className="back-button" onClick={() => navigate("/home")}>Back to Home</button>
    </div>
  );
};

export default PurchaseHistoryPage;