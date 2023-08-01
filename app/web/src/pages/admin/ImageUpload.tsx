'use client'

import React, { useState, useEffect } from "react";
import { Button, Flex, Input } from '@chakra-ui/react';
import Card from 'components/card/Card';

const ImageUpload = (props) => {
    const { start, result, url } = props;
    const [selectedFile, setSelectedFile] = useState(null);

    const fileChangeHandler = (e) => {
        setSelectedFile(e.target.files);
    }

    const handleSubmit = (e) => {

        console.log(selectedFile);
        const formData = new FormData();
        // formData.append(
        //     "file",
        //     selectedFile
        // )
        for (const file of selectedFile) {
            formData.append('files', file); // 'images' is the name of the field that will be used to access the files on the server-side
        }
        const reqOptions = {
            method: 'POST',
            body: formData,
            headers: {
                'ngrok-skip-browser-warning':true
            }
        };

        fetch(url + "predict", reqOptions)
            .then((Response) => {
                // uploadToParent(Response);
                return Response.json()
            }).then((data) => {
                result(data.file);
            })

    }

    return (
        <Card
            flexDirection='column'
            w='100%'
            px='0px'
            overflowX={{ sm: 'hidden', lg: 'hidden' }}>
            <Flex px='25px' justify='space-between' mb='2px' align='center' >
                <div>
                    <div className="row">
                        <div className="col-8">
                            <div id="input-group">
                                <label id="input-group__label" className="btn btn-default p-0" for="myInput">
                                    <input id="myInput" multiple="true" className="input-group__input" type="file" placeholder="Click" accept="image/*" onChange={fileChangeHandler}></input>
                                </label>
                            </div>
                        </div>

                        <div className="col-4">
                            <Button
                                variant='outline'
                                disabled={!selectedFile}
                                onClick={handleSubmit}
                                mt="20px"
                            >
                                Upload
                            </Button>
                        </div>
                    </div>
                </div>
            </Flex>
        </Card>
    );

};


export default ImageUpload;
