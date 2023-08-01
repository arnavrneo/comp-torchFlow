import React from 'react';
// Chakra imports
import { Box, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
// Custom components
import Card from 'components/card/Card';
// Assets
import { FaEthereum } from 'react-icons/fa';
import { Image } from 'components/image/Image';

export default function NFT(props: {
	image: string;
	name: string;
	author: string;
	date: string;
	price: string | number;
}) {
	const { image, name, author, date, price } = props;
	// Chakra Color Mode
	const textColor = useColorModeValue('brands.900', 'white');
	const bgItem = useColorModeValue(
		{ bg: 'white', boxShadow: '0px 40px 58px -20px rgba(112, 144, 176, 0.12)' },
		{ bg: 'navy.700', boxShadow: 'unset' }
	);
	const textColorDate = useColorModeValue('secondaryGray.600', 'white');
	return (
		<></>
	);
}
