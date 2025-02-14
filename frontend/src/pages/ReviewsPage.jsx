import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/ReviewsPage.css";

const ReviewsPage = () => {
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState({
    product_id: "",
    username: "",
    rating: "",
    comment: ""
  });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setIsLoading(true);
        const response = await fetch("http://localhost:4016/reviews?product_id=some_product_id", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch reviews");
        }

        const data = await response.json();
        setReviews(data);
      } catch (error) {
        console.error("Error fetching reviews:", error);
        setError("Failed to fetch reviews. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchReviews();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewReview((prevReview) => ({
      ...prevReview,
      [name]: value,
    }));
  };

  const handleAddReview = async () => {
    try {
      const response = await fetch("http://localhost:4016/reviews", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newReview),
      });

      if (!response.ok) {
        throw new Error("Failed to add review");
      }

      const addedReview = await response.json();
      setReviews((prevReviews) => [...prevReviews, addedReview]);
      setNewReview({ product_id: "", username: "", rating: "", comment: "" });
    } catch (error) {
      console.error("Error adding review:", error);
      setError("Failed to add review. Please try again later.");
    }
  };

  if (error) {
    return <div className="error-container"><p>{error}</p></div>;
  }

  return (
    <div className="reviews-container">
      <h2>Product Reviews</h2>
      {isLoading ? (
        <p className="loading">Loading...</p>
      ) : (
        <>
          <div className="add-review-form">
            <h3>Add New Review</h3>
            <input
              type="text"
              name="product_id"
              placeholder="Product ID"
              value={newReview.product_id}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={newReview.username}
              onChange={handleInputChange}
            />
            <input
              type="number"
              name="rating"
              placeholder="Rating"
              value={newReview.rating}
              onChange={handleInputChange}
            />
            <textarea
              name="comment"
              placeholder="Comment"
              value={newReview.comment}
              onChange={handleInputChange}
            />
            <button onClick={handleAddReview}>Add Review</button>
          </div>
          <ul className="reviews-list">
            {reviews.map((review) => (
              <li key={review._id} className="review-item">
                <span className="item-username">{review.username}</span>
                <span className="item-rating">Rating: {review.rating}</span>
                <span className="item-comment">Comment: {review.comment}</span>
              </li>
            ))}
          </ul>
        </>
      )}
      <button className="back-button" onClick={() => navigate("/home")}>Back to Home</button>
    </div>
  );
};

export default ReviewsPage;