import React, { useEffect, useState } from "react";
import {
    Box,
    TextField,
    Button,
    FormControlLabel,
    Checkbox,
    Link,
    Typography
} from "@mui/material";
import { useNavigate } from "react-router-dom";
  
function LoginPage() {
    const [metadataList, setMetadataList] = useState([]);
    const navigate = useNavigate();
    
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
                    label="User name"
                    placeholder="Enter your user name"
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
                
                <Button variant="contained" color="primary" fullWidth>
                    Login
                </Button>
                <Typography variant="body2" align="center" marginTop={2}>
                    Don't have an Account? <Link href="/register" onClick={() => navigate("/register") }>Register</Link>
                </Typography>
            </Box>

        </Box>
    );
}

export default LoginPage;