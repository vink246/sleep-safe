import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../../context/auth/authContext'

const PrivateRoute = ({ redirect, element }) => {
    const authContext = useContext(AuthContext);
    const { isAuthenticated, loading } = authContext;
    
    return !isAuthenticated && !loading ? <Navigate to={redirect} /> : element;
};
 
export default PrivateRoute;