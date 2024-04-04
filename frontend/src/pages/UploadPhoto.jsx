import React, { useState, useEffect } from 'react';
import { Alert, Grid, Paper, TextField, Button, Box, Autocomplete } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import Cookies from 'universal-cookie';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const UploadPhoto = () => {

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    }));

    const ruta_AWS = 'http://54.174.248.56:8000';
    const navigate = useNavigate();
    const cookies = new Cookies();
    const usuario_logeado = cookies.get('session');


    const [albumelegido, setAlbumelegido] = useState(null);
    const [error, setError] = useState(null);
    const [albums, setAlbums] = useState(null);
    const [fotoinfo, setFotoinfo] = useState({
        nombre: '',
        descripcion: '',
        foto: null,
        fotoPreview: null // Agregar estado para la vista previa de la imagen
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('name', fotoinfo.nombre);
        formData.append('photo', fotoinfo.foto);
        formData.append('description', fotoinfo.descripcion);
        formData.append('id', usuario_logeado?.id);

        const endpoint = await fetch(`${ruta_AWS}/upload`, {
            method: 'POST',
            body: formData
        });

        const resp = await endpoint.json();
        
        if (endpoint.status === 400) {
            setError(resp.mensaje);
        } else {
            alert(resp.mensaje)
            setError(null);
        }
    };

    const getAlbums = async () => {
        const data = {
          user: usuario_logeado?.id,
        };
    
        const endpoint = await fetch(`${ruta_AWS}/justalbums`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
    
        const resp = await endpoint.json();
        console.log(resp);
    
        if (endpoint.status === 400) {
          setError(resp.message);
        } else {
          setAlbums(resp);
          setError(null);
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFotoinfo({
            ...fotoinfo,
            foto: file,
            fotoPreview: URL.createObjectURL(file) // Crear URL temporal para la vista previa
        });
    };

    const volverPerfil = () => {
        navigate("/profile");
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <form onSubmit={handleSubmit}>
                <Grid container spacing={4} justifyContent="center" alignItems="center" style={{ marginTop: '20px' }}>
                    <Grid item xs={6}>
                        <Item >
                            <h1>Subir Foto</h1>
                        </Item>
                    </Grid>
                    <Grid item xs={2}>
                        <Item>
                            <Button onClick={volverPerfil} variant="contained"><ArrowBackIcon />
                                Volver
                            </Button>
                        </Item>
                    </Grid>
                </Grid>

                <Grid container spacing={4} justifyContent="center" alignItems="center" style={{ marginTop: '20px' }}>
                    <Grid item xs={4}>
                        <Item >
                            {fotoinfo.fotoPreview && <img src={fotoinfo.fotoPreview} alt="Foto" style={{ width: '100%', height: 'auto' }} />}
                        </Item>
                        <Paper elevation={3} style={{ padding: 20 }}>
                            <input type="file" accept="image/*" onChange={handleFileChange} />
                        </Paper>
                    </Grid>
                    <Grid item xs={4} >
                        <Paper elevation={3} style={{ padding: 20 }}>
                            <TextField
                                fullWidth
                                label="Nombre de la foto"
                                id="nombre"
                                name="nombre"
                                onChange={(e) => setFotoinfo({ ...fotoinfo, nombre: e.target.value })}
                                sx={{ marginBottom: '10px' }}
                            />
                            <TextField
                                fullWidth
                                label="Descripcion de la foto"
                                id="desc"
                                name="desc"
                                onChange={(e) => setFotoinfo({ ...fotoinfo, descripcion: e.target.value })}
                                sx={{ marginBottom: '10px' }}
                            />
                            <center>
                                <Button type="submit" variant="contained" color="success">
                                    Subir Foto
                                </Button>
                            </center>
                        </Paper>
                    </Grid>
                </Grid>
            </form>
            {error ? <Alert variant="filled" severity="error">{error}</Alert> : ''}
        </Box>
    );
};

export default UploadPhoto;
