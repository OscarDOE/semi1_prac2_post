import React, { useState, useRef, useEffect } from 'react';
import { Container, TextField, Button, Grid, Avatar, Paper, Box } from '@mui/material';
import { styled } from "@mui/material/styles";

const Chatbot = () => {
    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
        ...theme.typography.body2,
        padding: theme.spacing(2),
        textAlign: "center",
        color: theme.palette.text.secondary,
    }));

    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Generar un número de sesión aleatorio al cargar la página
        const sessionNumber = Math.floor(Math.random() * 1000);
        localStorage.setItem('sessionNumber', sessionNumber);
    }, []);

    

    const handleMessageSend = () => {
        if (inputText.trim() === '') return;

        const newMessages = [...messages, { text: inputText.trim(), sender: 'user' }];
        setMessages(newMessages);
        setInputText('');

        // Generar un número de sesión aleatorio
        const sessionNumber = localStorage.getItem('sessionNumber');

        const idd = String(sessionNumber)
        // Objeto que contiene los datos a enviar al backend
        const data = {
            message: inputText.trim(),
            session_id: idd
        };

        // Enviar los datos al backend
        fetch('http://54.174.248.56:8000/send_2bot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta del backend si es necesario
            console.log('Response from backend:', data);
            const concatenatedMessages = data.map(item => item.content).join('\n');
            const updatedMessages = [...newMessages, { text: concatenatedMessages, sender: 'chatbot' }];
            setMessages(updatedMessages);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleMessageSend();
        }
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Grid container spacing={2} justifyContent="center" alignItems="center" style={{ marginTop: "10px" }}>
                <Grid item xs={8}>
                    <Item>
                        <h1>Chatbot</h1>
                    </Item>
                </Grid>

                <Grid item xs={8}>
                    <Container style={{ maxWidth: '100%', backgroundColor: 'white', borderRadius: '10px', overflow: 'hidden', paddingTop: 10, paddingBottom: 10 }}>
                        <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #ccc', paddingTop: 5 }}>
                            <div style={{ padding: '10px' }}>
                                {messages.map((message, index) => (
                                    <div key={index} style={{ display: 'flex', alignItems: 'center', justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start', marginBottom: '10px' }}>
                                        {message.sender === 'user' ? (
                                            <Avatar alt="User Avatar" style={{ marginRight: '10px' }}>U</Avatar>
                                        ) : (
                                            <Avatar alt="Chatbot Avatar" style={{ marginRight: '10px' }}>B</Avatar>
                                        )}
                                        <div style={{ textAlign: 'left', maxWidth: '70%', wordWrap: 'break-word' }}>
                                            {message.text}
                                        </div>
                                    </div>
                                ))}
                                <div ref={messagesEndRef} />
                            </div>
                        </div>

                    </Container>

                    <Grid justifyContent="center" alignItems="center" >
                        <Grid item xs={12} style={{ marginTop: 20, backgroundColor: 'white', borderRadius: '10px', padding: 10 }}>
                            <TextField
                                style={{ width: '90%' }}
                                label="Type a message..."
                                variant="outlined"
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handleMessageSend}
                                style={{ marginLeft: '10px' }}
                            >
                                Send
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Chatbot;
