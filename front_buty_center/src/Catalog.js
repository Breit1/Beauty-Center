import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Catalog.css';

const Catalog = ({ details, username, token, onLogout }) => {
    const [commentContent, setCommentContent] = useState('');
    const [commentMark, setCommentMark] = useState(0);
    const [selectedCenter, setSelectedCenter] = useState(null);
    const [comments, setComments] = useState(() => {
        const savedComments = localStorage.getItem('comments');
        return savedComments ? JSON.parse(savedComments) : {};
    });
    const [centers, setCenters] = useState([]); // Add state for centers
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:8000/api/centers/')
            .then(response => {
                setCenters(response.data);
            })
            .catch(error => {
                console.error('Error fetching centers:', error);
            });
    }, [token]);


    useEffect(() => {
        console.log('Details updated:', details);
        if (details) {
            details.forEach(center => {
                fetchComments(center.id);
            });
        }
    }, [details]);

    useEffect(() => {
        localStorage.setItem('comments', JSON.stringify(comments));
    }, [comments]);

    const handleLogout = () => {
        onLogout();
        navigate('/');
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
            const response = await axios.post('http://localhost:8000/api/comments/', {
                center_id: selectedCenter,
                content: commentContent,
                mark: commentMark,
            }, {
                headers: token ? { 'Authorization': `Token ${token}` } : {}
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
                headers: token ? { 'Authorization': `Token ${token}` } : {}
            });
            console.log('Fetched comments for center', centerId, response.data);
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

    return (
        <div>
            <div className="unlogin-container">
                <div className="unlogin">
                    <div className="username"><div className="polzov">Пользователь:</div> {username}</div>
                    <button className="but-unlog" onClick={handleLogout}>Выйти</button>
                </div>
            </div>
            <div className="all-centers">
                <div className='text'>Все салоны</div>

                {centers && centers.length > 0 ? ( // Use centers state
                    <div className="centers-container">
                        {centers.map((center, id) => (
                            <div key={id} className="center-wrapper">
                                <div className='center-sens-comment'>
                                    <div className="center">
                                        <Link to={`/centers/${center.id}`} className="center-link">
                                            <div className="center-details">
                                                <h3 className="center-name">{center.name}</h3>
                                                <p className="center-phone">{center.phone}</p>
                                                <p className="center-address">{`${center.address.state}, ${center.address.city}, ${center.address.street} ${center.address.number}`}</p>
                                            </div>
                                        </Link>
                                    </div>

                                    {token && (
                                        <div className="comment-section">
                                            <div className='input-container'>
                                                <input
                                                    type="text"
                                                    value={selectedCenter === center.id ? commentContent : ''}
                                                    onChange={(e) => handleCommentChange(center.id, e.target.value)}
                                                    required
                                                />
                                                <label>Оставьте отзыв</label>
                                            </div>
                                            <div className="rating">
                                                {renderStars(center.id)}
                                            </div>
                                            {commentContent && selectedCenter === center.id && (
                                                <button className='send' type="submit" onClick={handleCommentSubmit}>Отправить</button>
                                            )}
                                        </div>
                                    )}

                                    {comments[center.id] && comments[center.id].length > 0 && (
                                        <div className="comments">
                                            <div className='comment-header'>Отзывы салона</div>
                                            <ul>
                                                {comments[center.id].map((comment, index) => (
                                                    <div className='comment' key={index}>
                                                        <p>{comment.content}</p>
                                                        <div>{renderCommentStars(comment.mark)}</div>
                                                        <p>От: {comment.user}</p>
                                                    </div>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
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

export default Catalog;
