import React, { Component } from "react";
import PropTypes from "prop-types";
import Grid from "@mui/material/Unstable_Grid2";
import Skeleton from "@mui/material/Skeleton";
import Box from "@mui/material/Box";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import { Container } from "@mui/material";
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));
interface IFileObject {
    id: number,
    name: string
}

type MyProps = {};
let MyState: Array<IFileObject> = [
    {
        id:1,
        name: 'item1'
    },
    {
        id:2,
        name: 'item2'
    },
    {
        id:3,
        name: 'item3'
    },
    {
        id:4,
        name: 'item3'
    },
    {
        id:5,
        name: 'item3'
    }
];

class FilesContainer extends Component<MyProps, Array<any>> {
  static propTypes: {};

  constructor(props: any) {
    super(props);
  }

  render() {
    return (
      <Container className="files_container">
          <Grid container spacing={1}>
                {MyState.map((item) => (
                    <Grid xs={3} key={item.id}>
                    <Item>
                        <h1> {item.name}</h1>
                        <Box sx={{ width: 300 }}>
                            <Skeleton />
                            <Skeleton animation="wave" />
                            <Skeleton animation={false} />
                        </Box>
                    </Item>
                    </Grid>
                ))}
          </Grid>
      </Container>
    );
  }
}

FilesContainer.propTypes = {};

export default FilesContainer;
