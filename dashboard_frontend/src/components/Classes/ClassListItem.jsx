import React from "react";
import {IconButton, ListItem, ListItemButton, ListItemText} from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

const ClassListItem = ({id, name, selected, setSelected, ...props}) => {

    return (
        <ListItem key={id} disablePadding secondaryAction={
            <IconButton component={"a"} href={'/school/class/' + id + '/'}>
                <ArrowForwardIosIcon/>
            </IconButton>

        }>

            <ListItemButton selected={selected} onClick={() => setSelected(id)}>
                <ListItemText primary={name}/>
            </ListItemButton>

        </ListItem>
    )
}

export default ClassListItem