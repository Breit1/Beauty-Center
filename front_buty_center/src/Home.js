import React, {useEffect, useState} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Home.css';
import personLogo from './svg/person.svg';
import logo from './svg/logo.svg';
import fon from './svg/fon-img.svg';
import {useRef} from 'react';

const Home = ({ details, username, onLogout }) => {
    const [showAccountOptions, setShowAccountOptions] = useState(false);
    const token = localStorage.getItem('token');
    const navigate = useNavigate();
    const [commentContent, setCommentContent] = useState('');
    const [commentMark, setCommentMark] = useState(0);
    const [selectedCenter, setSelectedCenter] = useState(null);
    const [comments, setComments] = useState(() => {
        const savedComments = localStorage.getItem('comments');
        return savedComments ? JSON.parse(savedComments) : {};
    });
    const [centersWithRatings, setCentersWithRatings] = useState(details);

    useEffect(() => {
        if (details) {
            details.forEach(center => {
                fetchComments(center.id);
            });
        }
    }, [details, token]);

    useEffect(() => {
        localStorage.setItem('comments', JSON.stringify(comments));
    }, [comments]);

    useEffect(() => {
        if (details) {
            const updatedCenters = details.map(center => {
                const centerComments = comments[center.id] || [];
                const averageRating = centerComments.length > 0 ?
                    (centerComments.reduce((acc, comment) => acc + comment.mark, 0) / centerComments.length).toFixed(1) : 'Нет';
                const commentsCount = centerComments.length;
                return { ...center, averageRating, commentsCount };
            });
            setCentersWithRatings(updatedCenters);
        }
    }, [comments, details]);

    const handleLogout = () => {
        onLogout();
        navigate('/');
    };

    const handleCommentSubmit = async (event) => {
        event.preventDefault();
        if (commentMark < 1 || commentMark > 5) {
            alert("Оценка должна быть от 1 до 5");
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/api/comments/', {
                center_id: selectedCenter,
                content: commentContent,
                mark: commentMark,
            }, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            console.log('Comment submitted:', response.data);

            setComments(prevComments => ({
                ...prevComments,
                [selectedCenter]: [...(prevComments[selectedCenter] || []), response.data]
            }));
            setCommentContent('');
            setCommentMark(0);
            setSelectedCenter(null);
        } catch (error) {
            console.error('Error submitting comment:', error);
        }
    };

    const fetchComments = async (centerId) => {
        try {
            const response = await axios.get(`http://localhost:8000/api/centers/${centerId}/comments/`, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            console.log('Fetched comments:', response.data);
            setComments(prevComments => ({
                ...prevComments,
                [centerId]: response.data
            }));
        } catch (error) {
            console.error('Error fetching comments:', error);
        }
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

    const toggleAccountOptions = () => {
        setShowAccountOptions(!showAccountOptions);
    };

    const ref = useRef(null);

    const handleClick = () => {
        ref.current?.scrollIntoView({behavior: 'smooth'});
    };

    const getRatingClass = (rating) => {
        if (rating === 'No ratings') return '';
        const parsedRating = parseFloat(rating);
        if (parsedRating <= 2.6) return 'rating-low';
        if (parsedRating <= 3.6) return 'rating-medium-low';
        if (parsedRating <= 4) return 'rating-medium-high';
        if (parsedRating <= 5) return 'rating-high';
        return '';
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

            <div className="fon">
                <div className="title">
                    Лучшие SPA & Beauty центры
                </div>
                <div className='pod-title'>
                    Откройте дверь к истинному блаженству
                </div>
                <div className='catalog-button' onClick={handleClick}>
                    Перейти в каталог
                </div>
                <div className='fon-img'>
                    <img src={fon} width="70%" height="100%" viewBox="0 0 200 200" alt="background"/>
                </div>
            </div>

            {/*  ---------Каталог---------  */}

            <div className="header-c" ref={ref}>Каталог</div>

            <div className="all-centers">
                {centersWithRatings && centersWithRatings.length > 0 ? (
                    <div className="centers-container">
                        {centersWithRatings.map((center, id) => (
                            <div key={id} className="center-wrapper">
                                <div className='center-sens-comment'>
                                    <div className="center">
                                        <Link to={`/centers/${center.id}`} className="center-link">
                                            <div className="center-details">
                                                <h3 className="center-name">{center.name}</h3>
                                                <p className="center-phone">{center.phone}</p>
                                                <p className="center-address">{`${center.address.state}, ${center.address.city}, ${center.address.street} ${center.address.number}`}</p>
                                                <div className="comments-r-c">
                                                    <p className={`center-rating ${getRatingClass(center.averageRating)}`}>{center.averageRating}</p>
                                                    <p className="center-comments">{center.commentsCount} отзыв.</p>
                                                </div>
                                            </div>
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>Центры не найдены или загрузка...</p>
                )}
            </div>
        </div>
    );
};

export default Home;
