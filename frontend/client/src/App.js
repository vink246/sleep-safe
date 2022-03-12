import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Home from './components/pages/Home';
import About from './components/pages/About';
import Register from './components/auth/Register';
import Login from './components/auth/Login';
import Alerts from './components/layout/Alerts';
import PrivateRoute from './components/routing/PrivateRoute';

import ContactState from './context/contact/ContactState';
import AuthState from './context/auth/AuthState';
import AlertState from './context/alert/AlertState'
import setAuthToken from './utils/setAuthToken';
import './App.css';

if (localStorage.token) {
  setAuthToken(localStorage.token);
}

const App = () => {
  return (
    <AuthState>
      <ContactState>
        <AlertState>
          <Router>
            <>
              <Navbar />
              <div className="container">
              <Alerts />  
                <Routes>
                  <Route  path='/' element={<PrivateRoute redirect="/login" element={<Home/>} />} />
                  <Route  path='/about' element={<About/>} />
                  <Route  path='/register' element={<Register/>} />
                  <Route  path='/login' element={<Login />} />
                </Routes>
              </div>
            </>
          </Router>
        </AlertState>
      </ContactState>
    </AuthState>
  );
}

export default App;
