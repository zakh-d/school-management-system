import React, {useEffect, useState} from "react";
import {Link, List, ListSubheader, Skeleton} from "@mui/material";
import ClassListItem from "./ClassListItem";

const ClassesList = ({selectedClassId, setSelectedClassId, ...props}) => {

    const [classes, setClasses] = useState([])
    const [isFetching, setFetching] = useState(false)

    useEffect(() => {
        setFetching(true)
        fetch('/api/v1/classes')
            .then(response => response.json())
            .then(data => {
                setFetching(false)
                setClasses(data)
        }).catch(() => {
            setFetching(false)
            setClasses([{name: 'Network Error', id: 1}])
        });

    }, [])

    const classesElements = classes.map((cls) => (<ClassListItem {...cls} selected={cls.id === selectedClassId} setSelected={setSelectedClassId} />))

    if (isFetching){
        return (
            <List subheader={<ListSubheader>Classes</ListSubheader>}>
                <Skeleton/>
                <Skeleton/>
                <Skeleton/>
            </List>

        )
    }
    return (
        <List subheader={<ListSubheader>Classes</ListSubheader>}>
            { classesElements }
        </List>
    )
}

export default ClassesList;