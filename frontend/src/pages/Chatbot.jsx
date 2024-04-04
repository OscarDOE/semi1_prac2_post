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

    const handleMessageSend = () => {
        if (inputText.trim() === '') return;

        const newMessages = [...messages, { text: inputText.trim(), sender: 'user' }];
        setMessages(newMessages);
        // Simulate response from the chatbot
        setTimeout(() => {
            const response = getChatbotResponse(inputText);
            const updatedMessages = [...newMessages, { text: response, sender: 'chatbot' }];
            setMessages(updatedMessages);
        }, 500);
        setInputText('');
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleMessageSend();
        }
    };

    const getChatbotResponse = (message) => {
        if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
            return "Hi there! How can I assist you?";
        } else if (message.toLowerCase().includes('how are you')) {
            return "I'm just a chatbot, but I'm doing well! How about you?";
        } else {
            return "I'm sorry, I'm not sure how to respond to that.";
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
                                 // Añadimos un margen izquierdo para separar el botón del TextField
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
