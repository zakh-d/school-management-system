import React, {useEffect, useState} from "react";
import {CircularProgress, Link, Skeleton, Table, TableBody, TableCell, TableHead} from "@mui/material";
import StudentTableItem from "./StudentTableItem";

const StudentList = ({selectedClassId, ...props}) => {

    const [students, setStudents] = useState([])
    const [isFetching, setFetching] = useState(false)

    useEffect(() => {
        if (selectedClassId) {
            setFetching(true)
        }
        fetch('/api/v1/classes/' + selectedClassId + '/students/')
            .then(response => response.json())
            .then(data => {
                setFetching(false)
                setStudents(data)
            }).catch(() => {
                setFetching(false)
            setStudents([])
        })
    }, [selectedClassId])

    const studentsElems = students.map(student => <StudentTableItem {...student}/>)
    if (isFetching){
        return (
            <>
                <Table>
                    <colgroup>
                      <col style={{width:'10%'}}/>
                      <col style={{width:'45%'}}/>
                      <col style={{width:'45%'}}/>
                   </colgroup>
                    <TableHead>
                        <TableCell>#</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>Surname</TableCell>
                    </TableHead>
                </Table>
                <Skeleton/>
                <Skeleton/>
                <Skeleton/>
            </>
        )
    }

    return (
        <Table>
            <TableHead>
                <TableCell>#</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Surname</TableCell>
            </TableHead>
            <TableBody>
                { studentsElems }
            </TableBody>
        </Table>
    )

}

export default StudentList;