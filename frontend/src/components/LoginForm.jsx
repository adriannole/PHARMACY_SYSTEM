import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/LoginForm.css"; 

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:4006/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("username", data.username);
        alert("¡Inicio de sesión exitoso!");
        navigate("/home");
      } else {
        alert(data.error || "¡Error en el inicio de sesión!");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      alert("Ocurrió un error. Por favor, inténtelo de nuevo más tarde.");
    }
  };

  return (
    <form onSubmit={handleLogin} className="login-form">
      <h2>Iniciar Sesión</h2>
      <input
        type="text"
        placeholder="Nombre de usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        className="login-input"
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        className="login-input"
      />
      <button type="submit" className="login-button">
        Iniciar Sesión
      </button>
      <p>
        <span onClick={() => navigate("/register")} className="register-link">
          Register
        </span>
      </p>
    </form>
  );
};

export default LoginForm;