// Chakra imports
import { Box, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
import BarChart from 'components/charts/BarChart';
import { ApexOptions } from "apexcharts";

type ApexGeneric = ApexOptions & any;
// Custom components
import Card from 'components/card/Card';
import C3Chart from 'react-c3js';
import 'c3/c3.css';
// Assets
import { RiArrowUpSFill } from 'react-icons/ri';

export default function DailyTraffic(props: { [x: string]: any }) {
	const { ...rest } = props;

	var data = [10, 15, 18, 9];
	var name = ["1", "2", "3", "4"];
	// console.log(rest.length);
	for (let s of Object.values(rest)[0]) {
		data.push(s["PRED_CT"]);
		name.push(s["IMG_ID"]);
	}
	// console.log(data);
	// barChartDataDailyTraffic[0]["data"] = data;


	// Chakra Color Mode
	const textColor = useColorModeValue('secondaryGray.900', 'white');
	return (
		<Card alignItems='center' flexDirection='column' w='100%' {...rest}>
			<Flex justify='space-between' align='start' px='10px' pt='5px' w='100%'>
				<Flex flexDirection='column' align='start' me='20px'>
					<Text color='secondaryGray.600' fontSize='sm' fontWeight='500'>
						Plastic Count Data
					</Text>
					<Flex align='end'>
						<Text color={textColor} fontSize='34px' fontWeight='700' lineHeight='100%'>

						</Text>
						<Text ms='6px' color='secondaryGray.600' fontSize='sm' fontWeight='500'>
							Visitors
						</Text>
					</Flex>
				</Flex>
				<Flex align='center' mt='4px'>
					<Icon as={RiArrowUpSFill} color='green.500' />
					<Text color='green.500' fontSize='sm' fontWeight='700'>
						+2.45%
					</Text>
				</Flex>
			</Flex>
			<Box h='300px' mt='auto'>

			</Box>
		</Card>
	);
}
