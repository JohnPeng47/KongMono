import { 
  Alert,
  Snackbar,
  AlertColor,
  SnackbarOrigin,
  SnackbarCloseReason
} from '@mui/material';
import { createContext } from 'use-context-selector';
import { useMemoObject } from '../hooks/useMemo';
import React, { SyntheticEvent, memo, useCallback, useState } from 'react';

export type AlertId = number & { __alertId: never };

export type ToastOptions = {
  message: string; 
  type: AlertColor;
  duration: number;
  position: SnackbarOrigin ;
};

interface AlertBoxContext {
  sendToast: (options: ToastOptions) => void;
}

export const AlertBoxContext = createContext<Readonly<AlertBoxContext>>({} as AlertBoxContext);
export const AlertBoxProvider = memo(({ children }: React.PropsWithChildren<unknown>) => {
  const [toast, setToast] = useState({
    open: false,              
    message: '',              
    type: 'info',             
    duration: 6000,           
    position: { 
      vertical: 'top', 
      horizontal: 'right' 
    } as SnackbarOrigin
  });

  const sendToast = useCallback((options: ToastOptions) => {
    setToast({
      open: true,
      message: options.message,
      type: options.type,
      duration: options.duration ? options.duration : 3000,
      position: options.position
    });
  }, []);

  const handleClose = (event: any, reason: any) => {
    if (reason === 'clickaway') {
      return;
    }
    setToast((prev) => ({ ...prev, open: false }));
  };

  const value = useMemoObject<AlertBoxContext>({
		sendToast
	});

return (
    <AlertBoxContext.Provider value={value}>
      <Snackbar
          open={toast.open}
          autoHideDuration={toast.duration}
          onClose={handleClose}
          anchorOrigin={toast.position}
        >
          {/* @ts-ignore */}
          <Alert onClose={handleClose} severity={toast.type}>
            {toast.message}
          </Alert>
      </Snackbar>
      {children}
    </AlertBoxContext.Provider>
  );
});
