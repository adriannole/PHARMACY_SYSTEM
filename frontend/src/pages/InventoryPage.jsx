import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/InventoryPage.css";

const InventoryPage = () => {
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    category: "",
    price: "",
    img: ""
  });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        setIsLoading(true);
        const response = await fetch("http://localhost:4015/inventory", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch inventory");
        }

        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Error fetching inventory:", error);
        setError("Failed to fetch inventory. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchInventory();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct((prevProduct) => ({
      ...prevProduct,
      [name]: value,
    }));
  };

  const handleAddProduct = async () => {
    try {
      const response = await fetch("http://localhost:4015/inventory", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newProduct),
      });

      if (!response.ok) {
        throw new Error("Failed to add product");
      }

      const addedProduct = await response.json();
      setProducts((prevProducts) => [...prevProducts, addedProduct]);
      setNewProduct({ name: "", category: "", price: "", img: "" });
    } catch (error) {
      console.error("Error adding product:", error);
      setError("Failed to add product. Please try again later.");
    }
  };

  const handleDeleteProduct = async (productId) => {
    try {
      const response = await fetch(`http://localhost:4015/inventory/${productId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete product");
      }

      setProducts((prevProducts) => prevProducts.filter((product) => product._id !== productId));
    } catch (error) {
      console.error("Error deleting product:", error);
      setError("Failed to delete product. Please try again later.");
    }
  };

  const handleUpdateProduct = async (productId, updatedFields) => {
    try {
      const response = await fetch(`http://localhost:4015/inventory/${productId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedFields),
      });

      if (!response.ok) {
        throw new Error("Failed to update product");
      }

      setProducts((prevProducts) =>
        prevProducts.map((product) =>
          product._id === productId ? { ...product, ...updatedFields } : product
        )
      );
    } catch (error) {
      console.error("Error updating product:", error);
      setError("Failed to update product. Please try again later.");
    }
  };

  if (error) {
    return <div className="error-container"><p>{error}</p></div>;
  }

  return (
    <div className="inventory-container">
      <h2>Inventory Management</h2>
      {isLoading ? (
        <p className="loading">Loading...</p>
      ) : (
        <>
          <div className="add-product-form">
            <h3>Add New Product</h3>
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={newProduct.name}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="category"
              placeholder="Category"
              value={newProduct.category}
              onChange={handleInputChange}
            />
            <input
              type="number"
              name="price"
              placeholder="Price"
              value={newProduct.price}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="img"
              placeholder="Image URL"
              value={newProduct.img}
              onChange={handleInputChange}
            />
            <button onClick={handleAddProduct}>Add Product</button>
          </div>
          <ul className="inventory-list">
            {products.map((product) => (
              <li key={product._id} className="inventory-item">
                <span className="item-name">{product.name}</span>
                <span className="item-category">Category: {product.category}</span>
                <span className="item-price">Price: ${product.price}</span>
                <span className="item-img">Image: <img src={product.img} alt={product.name} /></span>
                <button onClick={() => handleDeleteProduct(product._id)}>Delete</button>
                <button onClick={() => handleUpdateProduct(product._id, { name: "Updated Name" })}>Update</button>
              </li>
            ))}
          </ul>
        </>
      )}
      <button className="back-button" onClick={() => navigate("/home")}>Back to Home</button>
    </div>
  );
};

export default InventoryPage;