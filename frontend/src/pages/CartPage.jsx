import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/CartPage.css";

const CartPage = () => {
  const [cart, setCart] = useState([]); // Cart items
  const username = localStorage.getItem("username"); // Get username from local storage
  const [error, setError] = useState(null); // State to track errors
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const navigate = useNavigate(); // Navigation hook

  // Load cart from server
  useEffect(() => {
    const fetchCart = async () => {
      if (!username || username.trim() === "") {
        setError("Username not found. Please log in first.");
        return;
      }

      try {
        setIsLoading(true);
        const response = await fetch(`http://localhost:4005/get_cart/${username}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to load cart");
        }

        const data = await response.json();
        if (data.error) {
          setError(data.error); // Show error message if user not found
          return;
        }

        setCart(data.cart || []); // Update cart state with fetched data
      } catch (error) {
        console.error("Error fetching cart:", error);
        setError("Failed to fetch cart. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchCart();
  }, [username]);

  // Sort cart items by total price (price * quantity)
  const handleSortCart = async () => {
    try {
      const response = await fetch(`http://localhost:4010/sort_cart/${username}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to sort cart");
      }

      const data = await response.json();
      alert(data.message);
      setCart((prevCart) => [...prevCart].sort((a, b) => b.total_price - a.total_price));
    } catch (error) {
      console.error("Error sorting cart:", error);
      alert("Failed to sort cart. Please try again later.");
    }
  };

  // Delete a product from the cart
  const deleteProduct = async (productName) => {
    if (!username) {
      alert("No user logged in. Please log in first.");
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:4003/delete_product", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, product_name: productName }),
      });

      if (!response.ok) {
        throw new Error("Failed to delete product");
      }

      const data = await response.json();
      if (data.error) {
        alert(data.error);
        return;
      }

      // Remove the product from the cart state
      setCart((prevCart) => prevCart.filter((item) => item.product_name !== productName));
      alert(`Product '${productName}' has been deleted successfully.`);
    } catch (error) {
      console.error("Error deleting product:", error);
      alert("Failed to delete product. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  // Update quantity on the server
  const updateQuantity = async (productName, quantity) => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:4011/update_quantity", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          product_name: productName,
          quantity,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert(`Quantity for '${productName}' updated to ${quantity} successfully!`);
      } else {
        alert(`Error: ${data.error || "Failed to update quantity"}`);
      }
    } catch (error) {
      console.error("Error updating quantity:", error);
      alert("Failed to update quantity. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  // Handle local quantity change
  const handleQuantityChange = (productName, delta) => {
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.product_name === productName
          ? { ...item, quantity: Math.max(1, item.quantity + delta) }
          : item
      )
    );
  };

  // Reset the cart
  const resetCart = async () => {
    if (!username) {
      alert("No user logged in. Please log in first.");
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch(`http://localhost:4008/reset_cart/${username}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to reset cart");
      }

      const data = await response.json();
      if (data.error) {
        alert(data.error);
        return;
      }

      setCart([]); // Clear the cart state after resetting
      alert("Cart has been reset successfully.");
    } catch (error) {
      console.error("Error resetting cart:", error);
      alert("Failed to reset cart. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  // Proceed to payment (checkout)
  const proceedToPayment = async () => {
    try {
      const response = await fetch("http://localhost:4002/checkout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
      } else {
        alert(`Error: ${data.message || "Something went wrong."}`);
      }
    } catch (error) {
      console.error("Error during checkout:", error);
      alert("Failed to process payment. Please try again later.");
    }
  };

  // Calculate total price of items in the cart
  const calculateTotalPrice = () => {
    return cart
      .reduce((total, item) => total + item.price * item.quantity, 0)
      .toFixed(2);
  };

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="cart-container">
      <h2>{username ? `${username}'s Cart` : "Your Cart"}</h2>
      {isLoading ? (
        <p className="loading">Loading...</p>
      ) : cart.length === 0 ? (
        <p className="empty-cart">Your cart is empty.</p>
      ) : (
        <>
          <ul className="cart-list">
            {cart.map((item) => (
              <li key={item.product_name} className="cart-item">
                <div className="item-details">
                  <span className="item-name">{item.product_name}</span>
                  <span className="item-quantity">
                    Quantity: {item.quantity}
                    <button
                      className="quantity-button"
                      onClick={() => handleQuantityChange(item.product_name, -1)}
                    >
                      -
                    </button>
                    <button
                      className="quantity-button"
                      onClick={() => handleQuantityChange(item.product_name, 1)}
                    >
                      +
                    </button>
                  </span>
                  <span className="item-price">
                    $ {(item.price * item.quantity).toFixed(2)}
                  </span>
                </div>
                <div className="item-actions">
                  <button
                    className="update-button"
                    onClick={() => updateQuantity(item.product_name, item.quantity)}
                  >
                    Update Quantity
                  </button>
                  <button
                    className="delete-button"
                    onClick={() => deleteProduct(item.product_name)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <div className="cart-summary">
            <strong>Total: $ {calculateTotalPrice()}</strong>
          </div>
          <button className="sort-button" onClick={handleSortCart}>
            Sort Cart by Price
          </button>
          <button className="reset-button" onClick={resetCart}>
            Reset Cart
          </button>
          <button className="pay-button" onClick={proceedToPayment}>
            Proceed to Payment
          </button>
        </>
      )}
      <button className="back-button" onClick={() => navigate("/home")}>
        Back to Home
      </button>
    </div>
  );
};

export default CartPage;
