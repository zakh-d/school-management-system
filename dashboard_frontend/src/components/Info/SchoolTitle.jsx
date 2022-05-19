import React, {useEffect, useState} from 'react';
import {TextField, Typography} from "@mui/material";
import {getCookie} from "../../utils/cookies";

const SchoolTitle = ({text, ...props}) => {

    const [isEditing, setEditing] = useState(false);
    const [isFetching, setFetching] = useState(false);
    const [schoolName, setSchoolName] = useState(text)
    const [error, setError] = useState(false);

    useEffect(() => setSchoolName(text), [text])

    function handleChange(e){
        setSchoolName(e.target.value)
    }

    async function handleSubmit(e){

        if (e.target.value === ""){
            setError(true);
            return
        }

        const csrfToken = getCookie('csrftoken')

        setEditing(false)

        setFetching(true)
        const response = await fetch('/api/v1/school/', {
            method: 'PUT',
            body: JSON.stringify({
                name: schoolName
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFTOKEN': csrfToken
            }
        })

        if (response.status === 200){
            setFetching(false)
        }

    }

    if (isEditing && !isFetching) {
        return (
            <>
                <TextField fullWidth error={error} helperText={ error ? "This field may not be blank" : ""} variant="filled" label="School Name" onBlur={handleSubmit} onChange={handleChange} type="text" value={schoolName} autoFocus/>
            </>
        )
    }

    return (
        <>
            <Typography onDoubleClick={() => setEditing(true)} color={isFetching ? 'gray' : 'black'} variant="h4">{schoolName}</Typography>
        </>
    )
}

export default SchoolTitle;