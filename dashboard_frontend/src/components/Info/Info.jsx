import React, {useEffect, useState} from "react";
import {Box, Divider, Paper, Typography} from "@mui/material";
import SchoolTitle from "./SchoolTitle";

const Info = (props) => {

    const [info, setInfo] = useState({})

    useEffect(() => {
        fetch('/api/v1/auth/me/')
            .then(res => res.json())
            .then(data => {
                setInfo(data)
            })
    }, [])

    return (
        <Paper elevation={3}>
            <Box p={4}>
                { info.role === 'Administration Member' ?
                    <SchoolTitle text={info.school}/> :
                    <Typography variant="h4">{info.school}</Typography>
                }
                <Typography variant="h5">{info.first_name} {info.last_name} | {info.role}</Typography>
            </Box>
        </Paper>
    )
}

export default Info;