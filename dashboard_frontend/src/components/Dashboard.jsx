import React, {useEffect, useState} from "react";
import Info from "./Info/Info";
import ClassesList from "./Classes/ClassesList";
import {Box, Grid} from "@mui/material";
import StudentList from "./Students/StudentList";

const Dashboard = (props) => {

    const [selectedClassId, setSelectedClassId] = useState(null)

    useEffect(() => {
        document.title = 'Dashboard'
    }, [])

    return (
        <div>
            <Box mb={2}>
                <Info/>
            </Box>

            <Grid container spacing={2}>
                <Grid item md={3} xs={12}>
                    <ClassesList selectedClassId={selectedClassId} setSelectedClassId={setSelectedClassId}/>
                </Grid>

                <Grid item md={9} xs={12}>
                    <StudentList selectedClassId={selectedClassId}/>
                </Grid>
            </Grid>
        </div>
    )
}

export default Dashboard;