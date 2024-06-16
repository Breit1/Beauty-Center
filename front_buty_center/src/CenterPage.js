import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './CenterPage.css';
import logo from "./svg/logo.svg";
import personLogo from "./svg/person.svg";
import fonServices from "./svg/fon-services.svg";
import fon from "./svg/fon-img.svg";

const CenterPage = ({ username, onLogout }) => {
    const [showAccountOptions, setShowAccountOptions] = useState(false);
    const { centerId } = useParams();
    const [center, setCenter] = useState(null);
    const [services, setServices] = useState([]);
    const [comments, setComments] = useState([]);
    const [commentContent, setCommentContent] = useState('');
    const [commentMark, setCommentMark] = useState(0);
    const token = localStorage.getItem('token');
    const navigate = useNavigate();
    const [selectedCenter, setSelectedCenter] = useState(null);

    useEffect(() => {
        const fetchCenterData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/centers/${centerId}/`);
                const data = await response.json();
                setCenter(data);
            } catch (error) {
                console.error('Error fetching center data:', error);
            }
        };

        const fetchCenterServices = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/center-services/?center=${centerId}`);
                const data = await response.json();
                setServices(data.filter(service => service.center === centerId));
            } catch (error) {
                console.error('Error fetching services:', error);
            }
        };

        const fetchComments = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/centers/${centerId}/comments/`);
                const data = await response.json();
                console.log('Fetched comments:', data); // Для отладки
                setComments(Array.isArray(data) ? data : []);
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        };

        fetchCenterData();
        fetchCenterServices();
        fetchComments();
    }, [centerId]);

    const handleLogout = () => {
        onLogout();
        navigate('/'); // Перенаправляем на страницу регистрации
    };

    const handleCommentSubmit = async (event) => {
        event.preventDefault();
        if (!token) {
            alert("Пожалуйста, войдите в систему, чтобы оставить комментарий.");
            return;
        }
        if (commentMark < 1 || commentMark > 5) {
            alert("Оценка должна быть от 1 до 5");
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/comments/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
                body: JSON.stringify({
                    center_id: centerId,
                    content: commentContent,
                    mark: commentMark,
                }),
            });

            const newComment = await response.json();
            console.log('Submitted comment:', newComment); // Для отладки
            setComments(prevComments => [...prevComments, newComment]);
            setCommentContent('');
            setCommentMark(0);
        } catch (error) {
            console.error('Error submitting comment:', error);
        }
    };

    if (!center) {
        return <div>Loading...</div>;
    }

    const ButtonReturn = () => {
        navigate('/home');
    };

    const toggleAccountOptions = () => {
        setShowAccountOptions(!showAccountOptions);
    };

    const handleCommentChange = (centerId, content) => {
        setCommentContent(content);
        setSelectedCenter(centerId);
    };

    const handleStarClick = (centerId, mark) => {
        setCommentMark(mark);
        setSelectedCenter(centerId);
    };

    const renderStars = (centerId) => {
        return [1, 2, 3, 4, 5].map(star => (
            <span
                key={star}
                className={`star ${commentMark >= star ? 'filled' : ''}`}
                onClick={() => handleStarClick(centerId, star)}
            >
                ★
            </span>
        ));
    };

    const renderCommentStars = (mark) => {
        return [1, 2, 3, 4, 5].map(star => (
            <span
                key={star}
                className={`star ${mark >= star ? 'filled' : ''}`}
            >
                ★
            </span>
        ));
    };

    return (
        <div>
            <div className="header">
                <div className="logo">
                    <img src={logo} alt="logo"/>
                </div>
                <div className="header-right">
                    <div className="links">
                        <a className='catalog' href='/Catalog'>Каталог</a>
                        <a className='about' href='/Catalog'>О нас</a>
                        <a className='contacts' href='/Catalog'>Контакты</a>
                    </div>
                    <div className="account" onClick={toggleAccountOptions}>
                        <img src={personLogo} alt="account"/>
                        {showAccountOptions && (
                            <div className="account-options">
                                <div className="username">Пользователь: {username}</div>
                                <button className="but-unlog" onClick={handleLogout}>Выйти</button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <button className="to-top" onClick={ButtonReturn}></button>
            <div className="fon-cp">
                <div className="title-cp">
                    Салон {center.name}
                </div>
                <div className='fon-img-cp'>
                    <img src={fonServices} width="100%" height="100%" viewBox="0 0 200 200" alt="background"/>
                </div>
            </div>
            <div className="block-up"></div>

            <div className="block-container">
                <div className="side-block block-left"></div>
                <div className="main-content">
                    <div className="services-section">
                        <div className="center-details-p">
                            <h1>Услуги салона</h1>
                            <p className="center-phone">{center.phone}</p>
                            <p className="center-address">
                                {center.address ? (
                                    `${center.address.state}, ${center.address.city}, ${center.address.street} ${center.address.number}`
                                ) : (
                                    'Address not available'
                                )}
                            </p>
                        </div>
                        <div className="services-grid">
                            {services.map(service => (
                                <div className="center-p" key={service.id}>
                                    <div className="center-details">
                                        <h3>{service.service.name}</h3>
                                        <p>Категория: {service.service.category}</p>
                                        <p>Описание: {service.description}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
                <div className="side-block block-right"></div>
            </div>
            <div className="block-down"></div>
            <div className="comment-section">
                <h2>Отзывы</h2>
                {token && (
                    <div className="inp-com">
                        <div className="form__group field">
                            <input
                                value={commentContent}
                                onChange={(e) => setCommentContent(e.target.value)}
                                placeholder="Ваш комментарий"
                                required
                                className="form__field"
                            />
                            <label htmlFor="name" className="form__label">Ваш отзыв</label>
                            <div className="rating">
                                {renderStars(center.id)}
                            </div>
                            {commentContent && selectedCenter === center.id && (
                                <button className='send' type="submit" onClick={handleCommentSubmit}>Отправить</button>
                            )}
                        </div>
                    </div>
                )}
                <ul className="comment-list">
                    {comments.map(comment => (
                        <li key={comment.id} className="comment-item">
                            <p>От: {comment.user}</p>
                            <p className="comment-content">{comment.content}</p>
                            <div className="rating">
                                {renderCommentStars(comment.mark)}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default CenterPage;
