import './Register.css';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLogin, setIsLogin] = useState(false);
    const navigate = useNavigate();

    const handleRegister = async (event) => {
        event.preventDefault();
        setError('');
        setSuccess('');

        const passwordRegex = /^(?=.*[a-zA-Z]).{7,}$/;
        if (!passwordRegex.test(password)) {
            setError('Пароль слишком простой. Пароль должен быть не менее 7 знаков и с использованием букв.');
            return;
        }

        try {
            await axios.post('http://localhost:8000/api/register/', {
                username: username,
                password: password,
                email: email,
            });
            setSuccess('Регистрация прошла успешно!');

            try {
                const response = await axios.post('http://localhost:8000/api/api-token-auth/', {
                    username: username,
                    password: password,
                });
                const token = response.data.token;
                onLogin(token, username);
                navigate('/home');
            } catch (loginError) {
                setError('Регистрация прошла успешно, но автоматический вход не удался. Пожалуйста, войдите вручную.');
            }
        } catch (error) {
            setError('Произошла ошибка. Возможно, такой пользователь уже существует.');
        }
    };

    const handleLogin = async (event) => {
        event.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await axios.post('http://localhost:8000/api/api-token-auth/', {
                username: username,
                password: password,
            });
            const token = response.data.token;
            setSuccess('Вход выполнен успешно! Токен: ' + token);
            onLogin(token, username);
            navigate('/home');
        } catch (error) {
            setError('Неверное имя пользователя или пароль.');
        }
    };

    const handleGuestLogin = (event) => {
        event.preventDefault();
        const guestUsername = 'guest';
        console.log("Guest login:", guestUsername);
        onLogin('', guestUsername);
        navigate('/home');
    };

    return (
        <div className="ring">
            <i style={{ '--clr': '#5D806E' }}></i>
            <i style={{ '--clr': '#5D806E' }}></i>
            <i style={{ '--clr': '#5D806E' }}></i>
            <div className="login">
                <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
                <form className="inputBx" onSubmit={isLogin ? handleLogin : handleRegister}>
                    <input type="text" placeholder="Имя пользователя" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    {!isLogin && <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />}
                    <input type="submit" value={isLogin ? 'Войти' : 'Зарегистрироваться'} />
                </form>
                <div className="links">
                    <a href='#' onClick={handleGuestLogin} >Войти как гость</a>
                    <a href="#" onClick={() => setIsLogin(!isLogin)}>{isLogin ? 'Регистрация' : 'Войти'}</a>
                </div>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}
            </div>
        </div>
    );
};

export default Register;
