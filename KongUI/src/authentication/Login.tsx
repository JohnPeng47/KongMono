import React, { useEffect, useState } from "react";
import { useContext } from "use-context-selector";
import {
    Box,
    TextField,
    Button,
    Link,
    Typography
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { BackendContext } from "../concept_map/provider/backendProvider";
import { AlertBoxContext } from "../common/provider/AlertBoxProvider";
  
function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();
    const handleChangeEvent = (event, setVal) => {
        setVal(event.target.value);
    } 

    const { sendToast } = useContext(AlertBoxContext);
    const { backend } = useContext(BackendContext);

    const Login = (email: string, password: string): void => {
        backend.login(email, password)
            .then((res) => {
                navigate("/");
            })
            .catch((err) => {
                sendToast(err, "error");
            })
    } 
    
    return (
        <Box display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
        >
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                height="100vh"
                width="505px"
            >
                <Typography variant="h5" gutterBottom>
                Welcome!
                </Typography>
                
                <Typography variant="subtitle1" gutterBottom>
                Sign in to
                </Typography>

                <TextField
                    variant="outlined"
                    margin="normal"
                    fullWidth
                    label="Email"
                    placeholder="Enter your email"
                    onChange={(e) => handleChangeEvent(e, setEmail)}
                />
                
                <TextField
                    variant="outlined"
                    margin="normal"
                    fullWidth
                    type="password"
                    label="Password"
                    placeholder="Enter your Password"
                    InputProps={{
                        endAdornment: <span>👁️</span> // This can be replaced with a proper icon component
                    }}
                    onChange={(e) => handleChangeEvent(e, setPassword)}
                />

                {/* <Box display="flex" justifyContent="space-between" width="100%" marginY={2}>
                    <FormControlLabel
                        control={<Checkbox color="primary" />}
                        label="Remember me"
                    />
                    <Link href="#" variant="body2">
                        Forgot Password?
                    </Link>
                </Box> */}
                
                <Button 
                    variant="contained" 
                    color="primary" 
                    fullWidth 
                    onClick={(_) => Login(email, password)}>
                    Login
                </Button>
                <Typography variant="body2" align="center" marginTop={2}>
                    Dont have an Account? 
                    <Link href="/register" 
                        onClick={() => navigate("/register")}>Register</Link>
                </Typography>
            </Box>

        </Box>
    );
}


export default LoginPage;