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
  
function RegistrationPage() {
    const [metadataList, setMetadataList] = useState([]);
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

                <Button variant="contained" color="primary" fullWidth>
                    Register
                </Button>
            </Box>
        </Box>
    );
}

export default RegistrationPage;