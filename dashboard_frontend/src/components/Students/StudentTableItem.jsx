import React from "react";
import {TableCell, TableRow} from "@mui/material";

const StudentTableItem = ({id, order_in_class, first_name, last_name, ...props}) => {

    return (
        <TableRow key={id}>
            <TableCell>{order_in_class}</TableCell>
            <TableCell>{first_name}</TableCell>
            <TableCell>{last_name}</TableCell>
        </TableRow>
    )
}

export default StudentTableItem;