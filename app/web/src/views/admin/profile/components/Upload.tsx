// Chakra imports
import { Box, Button, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
// Custom components
import Card from 'components/card/Card';
// Assets
import { MdUpload } from 'react-icons/md';
import Dropzone from 'views/admin/profile/components/Dropzone';

export default function Upload(props: { used?: number; total?: number; [x: string]: any }) {
	const { used, total, ...rest } = props;
	// Chakra Color Mode
	const textColorPrimary = useColorModeValue('secondaryGray.900', 'white');
	const brandColor = useColorModeValue('brand.500', 'white');
	const textColorSecondary = 'gray.400';
	return (
<></>
	);
}
