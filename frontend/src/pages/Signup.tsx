import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom"; // Add Link import
import { AuthContext } from "../context/AuthContext";

const Signup: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("editor");
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await auth?.signup(email, password, name, role);
      navigate("/");
    } catch (error) {
      alert(`Signup failed ${error}`);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        padding: "20px",
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "40px",
          borderRadius: "12px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
          width: "100%",
          maxWidth: "400px",
          textAlign: "center",
        }}
      >
        <h2
          style={{
            fontSize: "2rem",
            marginBottom: "20px",
            color: "#333",
            fontWeight: "600",
          }}
        >
          Signup
        </h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontSize: "1rem",
                color: "#555",
                fontWeight: "500",
              }}
            >
              Email:
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "12px",
                fontSize: "1rem",
                border: "1px solid #ccc",
                borderRadius: "6px",
                outline: "none",
                transition: "border-color 0.3s",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#007bff")}
              onBlur={(e) => (e.target.style.borderColor = "#ccc")}
            />
          </div>
          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontSize: "1rem",
                color: "#555",
                fontWeight: "500",
              }}
            >
              Password:
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "12px",
                fontSize: "1rem",
                border: "1px solid #ccc",
                borderRadius: "6px",
                outline: "none",
                transition: "border-color 0.3s",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#007bff")}
              onBlur={(e) => (e.target.style.borderColor = "#ccc")}
            />
          </div>
          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontSize: "1rem",
                color: "#555",
                fontWeight: "500",
              }}
            >
              Name:
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "12px",
                fontSize: "1rem",
                border: "1px solid #ccc",
                borderRadius: "6px",
                outline: "none",
                transition: "border-color 0.3s",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#007bff")}
              onBlur={(e) => (e.target.style.borderColor = "#ccc")}
            />
          </div>
          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontSize: "1rem",
                color: "#555",
                fontWeight: "500",
              }}
            >
              Role:
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              style={{
                width: "100%",
                padding: "12px",
                fontSize: "1rem",
                border: "1px solid #ccc",
                borderRadius: "6px",
                outline: "none",
                background: "#fff",
                transition: "border-color 0.3s",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#007bff")}
              onBlur={(e) => (e.target.style.borderColor = "#ccc")}
            >
              <option value="editor">Editor</option>
              <option value="owner">Owner</option>
            </select>
          </div>
          <button
            type="submit"
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "1rem",
              background: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              transition: "background 0.3s",
            }}
            onMouseOver={(e) => (e.currentTarget.style.background = "#0056b3")}
            onMouseOut={(e) => (e.currentTarget.style.background = "#007bff")}
          >
            Signup
          </button>
        </form>
        <p
          style={{
            marginTop: "20px",
            fontSize: "0.9rem",
            color: "#555",
          }}
        >
          Already have an account?{" "}
          <Link
            to="/login"
            style={{
              color: "#007bff",
              textDecoration: "none",
              fontWeight: "500",
            }}
            onMouseOver={(e) =>
              (e.currentTarget.style.textDecoration = "underline")
            }
            onMouseOut={(e) => (e.currentTarget.style.textDecoration = "none")}
          >
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
