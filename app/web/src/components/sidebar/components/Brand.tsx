// Chakra imports
import { Flex, useColorModeValue, Text } from '@chakra-ui/react';

// Custom components
import { HSeparator } from 'components/separator/Separator';

export function SidebarBrand() {
	//   Chakra color mode

	return (
		<Flex alignItems='center' flexDirection='column'>
			<Text as="u" fontSize="xl">Team</Text>
			<Text
				as='b'
				fontSize='4xl'
			>torchFlow </Text>
			<HSeparator mb='20px' />
		</Flex>
	);
}

export default SidebarBrand;
