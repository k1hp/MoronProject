import React, { useState } from 'react';
const App = () => {
    const [isUsername, setIsUsername] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const toggleForm = () => {
        setIsUsername((prev) => !prev);
        setEmail('');
        setPassword('');
        setErrorMessage('');
    };

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('https://your-api-url.com/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ Username, password }),
            });

            if (!response.ok) {
                throw new Error('Неправильные данные. Попробуйте снова.');
            }

            const data = await response.json();
            alert('Успешный вход!');
            history.push('/website pages/website.html');
        } catch (error) {
            setErrorMessage(error.message);
        }
    };

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('https://your-api-url.com/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, Username }),
            });

            if (!response.ok) {
                throw new Error('Ошибка регистрации. Попробуйте снова.');
            }

            alert('Регистрация успешна! Теперь вы можете войти.');
            toggleForm();
        } catch (error) {
            setErrorMessage(error.message);
        }
    };
    
};

export default App;