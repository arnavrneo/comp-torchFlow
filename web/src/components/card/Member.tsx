// Chakra imports
import { Avatar, Flex, useColorModeValue, Icon, Text } from '@chakra-ui/react';
// Custom components
import Card from 'components/card/Card';
// Custom icons
import { IoEllipsisVertical } from 'react-icons/io5';

export default function Default(props: { avatar: string; name: string; job: string }) {
	const { avatar, name, job, ...rest } = props;
	const textColor = useColorModeValue('secondaryGray.900', 'white');
	const bg = useColorModeValue('white', '#1B254B');
	const shadow = useColorModeValue('0px 18px 40px rgba(112, 144, 176, 0.12)', 'none');

	return (
<></>
	);
}
