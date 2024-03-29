import Drawer from '@mui/material/Drawer';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import List from '@mui/material/List';
import TextField from '@mui/material/TextField';
import { IconButton, Stack } from '@mui/material';

import { UseStateDispatch } from "../utils/types";
import { Node } from "reactflow";
import styled from 'styled-components';
import { RFNodeData } from '../../common/common-types';

type SideMenuProps = {
    // what?
    children: React.ReactNode;
    data: RFNodeData;
    setIsOpen: UseStateDispatch<boolean>;
    isOpen: boolean;
}

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    // padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    // ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  }));
  

export default function SideMenu(props: SideMenuProps) {
    const { setIsOpen, isOpen } = props;
    console.log("Re-rendering with: ", props.data);

    return (
        <div>
            <Drawer
                anchor='right'
                open={props.isOpen}
                variant='persistent'
                // onClose={setIsOpen(false)}
            >
            <DrawerHeader>
                <IconButton onClick={() => setIsOpen(!isOpen)}>
                     <ChevronRightIcon />
                </IconButton>
            </DrawerHeader>
            <Stack>
                <TextField
                    value={props.data ? props.data.title : ""}
                    variant="standard"
                />
                <TextField
                    id="standard-multiline-static"
                    multiline
                    rows={4}
                    value={props.data ? props.data.description : ""}
                    variant="standard"
                />
            </Stack>
            </Drawer>
        </div>
    );
}
