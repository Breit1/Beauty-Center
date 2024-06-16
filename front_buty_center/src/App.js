import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Register from './Register';
import Catalog from './Catalog';
import axios from 'axios';
import CenterPage from './CenterPage';
import Home from './Home';

const App = () => {
    const [centers, setCenters] = useState([]);
    const [services, setServices] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [comments, setComments] = useState([]);
    const [serviceCenters, setServiceCenters] = useState([]);
    const [token, setToken] = useState(localStorage.getItem('token') || '');
    const [username, setUsername] = useState(localStorage.getItem('username') || '');

    useEffect(() => {
        axios.get('http://localhost:8000/api/centers/')
            .then(res => {
                setCenters(res.data);
            })
            .catch(err => {
                console.log(err);
            });

        axios.get('http://localhost:8000/api/services/')
            .then(res => {
                setServices(res.data);
            })
            .catch(err => {
                console.log(err);
            });

        axios.get('http://localhost:8000/api/addresses/')
            .then(res => {
                setAddresses(res.data);
            })
            .catch(err => {
                console.log(err);
            });

        axios.get('http://localhost:8000/api/center-services/')
            .then(res => {
                setServiceCenters(res.data);
            })
            .catch(err => {
                console.log(err);
            });


        axios.get('http://localhost:8000/api/comments/', )
            .then(res => {
                setComments(res.data);
            })
            .catch(err => {
                console.log(err);
            });

    }, [token]);


    const handleLogin = (token, username) => {
        setToken(token);
        setUsername(username);
        localStorage.setItem('token', token);
        localStorage.setItem('username', username);
    };

    const handleLogout = () => {
        setToken('');
        setUsername('');
        setCenters([]);
        setServices([]);
        setAddresses([]);
        setComments([]);  // Очистка комментариев при выходе из аккаунта
        setServiceCenters([]);
        localStorage.removeItem('token');
        localStorage.removeItem('username');
    };

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Register onLogin={handleLogin} />} />
                <Route path="/catalog" element={<Catalog details={centers} username={username} onLogout={handleLogout} token={token} />} />
                <Route path="/home" element={<Home details={centers} username={username} onLogout={handleLogout} />} />
                <Route path="/centers/:centerId" element={<CenterPage username={username} onLogout={handleLogout} centers={centers} services={services} />} />
            </Routes>
        </Router>
    );
};

export default App;
