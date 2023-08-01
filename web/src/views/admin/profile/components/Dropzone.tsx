// Chakra imports
import { Button, Flex, useColorModeValue } from '@chakra-ui/react';
// Assets
import { useDropzone } from 'react-dropzone';

function Dropzone(props: { content: JSX.Element | string; [x: string]: any }) {
	const { content, ...rest } = props;
	const { getRootProps, getInputProps } = useDropzone();
	const bg = useColorModeValue('gray.100', 'navy.700');
	const borderColor = useColorModeValue('secondaryGray.100', 'whiteAlpha.100');
	return (
<></>
	);
}

export default Dropzone;
