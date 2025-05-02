import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const PrivateRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const auth = useContext(AuthContext);

  if (auth?.isLoading) {
    return <div>Loading...</div>; // Show loading state while verifying token
  }

  return auth?.token && auth?.user ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
