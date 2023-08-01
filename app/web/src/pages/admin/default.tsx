import {
  Avatar,
  Box,
  Flex,
  FormLabel,
  Icon,
  Select,
  Text,
  SimpleGrid,
  Image,
  Center,
  Input,
  useColorModeValue,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  Tooltip,
  SliderThumb,
  SliderMark,
} from '@chakra-ui/react'
// Assets
// Custom components
import MiniStatistics from 'components/card/MiniStatistics'
import IconBox from 'components/icons/IconBox'
import {
  MdAttachMoney,
  MdBarChart,
  MdStackedBarChart,
  MdAddAlert
} from 'react-icons/md'
import ComplexTable from 'views/admin/default/components/ComplexTable'
import {
  columnsDataCheck,
  columnsDataComplex,
  TableData
} from 'views/admin/default/variables/columnsData'
import AdminLayout from 'layouts/admin'
import ImageUpload from './ImageUpload'
import { useEffect, useRef, useState } from 'react'
import getDistance from 'geolib/es/getDistance';
import Card from 'components/card/Card';

export default function UserReports() {
  // Chakra Color Mode

  const brandColor = useColorModeValue('brand.500', 'white')
  const boxBg = useColorModeValue('secondaryGray.300', 'whiteAlpha.100')

  const [data, setData] = useState([]);
  const [url, setUrl] = useState('');

  const [lat, setLat] = useState(0);
  const [long, setLong] = useState(0);
  const [thresh, setThresh] = useState(0);
  const [sliderValue, setSliderValue] = useState(5);
  const [showTooltip, setShowTooltip] = useState(false);


  const totalPred = (data: any[]) => {
    let count = 0;
    for (const i of data) {
      // let coord = i.GEO_TAG_URL.toString().split("=")[1].split("%2C");
      // i['GEO_TAG_URL'] = i["GEO_TAG_URL"].split("=")[1].split("%2C");
      // console.log(i);
      // console.log(i.GEO_TAG_URL.split("=")[1].split("%2C"));
      count += i.PRED_CT;
      // count = i["GEO_TAG_URL"].split("=")[1].split("%2C");
      i.coord = getDistance({
        latitude: lat, longitude: long
      }, {
        latitude: i["GEO_TAG_URL"].split("=")[1].split("%2C")[0],
        longitude: i["GEO_TAG_URL"].split("=")[1].split("%2C")[1]
      }) * 0.001;
      i.mail = i["PRED_CT"];
    };
    return count;
  };

  // For using navigator, need to wrap around useEffect, thats how nextjs works
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(function (position) {
      setLat(position.coords.latitude);
      setLong(position.coords.longitude);
    })
  });

  return (
    <AdminLayout>
      <Box pt={{ base: '130px', md: '80px', xl: '80px' }}>
        <>
          <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px' mt='20px'>

            <MiniStatistics
              startContent={
                <div>
                  <Text mb='8px'>Server Url: </Text>
                  <Input
                    focusBorderColor='purple.500'
                    variant="filled"
                    placeholder='Enter the server url'
                    type="text"
                    htmlSize={200}
                    onChange={e => setUrl(e.target.value)} />
                </div>
              }
              name=''
              value=''
            />
            <MiniStatistics
              startContent={
                <ImageUpload
                  start={data}
                  result={setData}
                  url={url}
                />
              }
              name='Supported type'
              value='jpg/jpeg'
            />
          </SimpleGrid>
          <SimpleGrid
            columns={{ base: 1, md: 2, lg: 2 }}
            gap='20px'
            mb='20px'
          >
            <MiniStatistics
              startContent={
                <IconBox
                  w='56px'
                  h='56px'
                  bg={boxBg}
                  icon={
                    <Icon
                      w='32px'
                      h='32px'
                      as={MdStackedBarChart}
                      color={brandColor}
                    />
                  }
                />
              }
              name='Total Plastics Predicted'
              value={totalPred(data)}
            />
            <MiniStatistics
              startContent={
                <IconBox
                  w='56px'
                  h='56px'
                  bg={boxBg}
                  icon={
                    <Icon
                      w='32px'
                      h='32px'
                      as={MdAddAlert}
                      color='tomato'
                    />
                  }
                />
              }
              name='Alert Threshold'
              value={
                <div>
                  <Slider aria-label='slider-ex-4' mt="5px" onChange={(val) => setThresh(val)} defaultValue={10} min={0} max={100} onMouseEnter={() => setShowTooltip(true)} onMouseLeave={() => setShowTooltip(false)}>
                    <SliderTrack bg='red.100'>
                      <SliderFilledTrack bg='blue' />
                    </SliderTrack>
                    <Tooltip
                      hasArrow
                      bg='teal.500'
                      color='white'
                      placement='top'
                      isOpen={showTooltip}
                      label={`${thresh}`}
                    >
                      <SliderThumb boxSize={6}>
                        <Box color='tomato' as={MdAddAlert} />
                      </SliderThumb>
                    </Tooltip>

                  </Slider>
                </div>}
            />
          </SimpleGrid>
          <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px'>
            <ComplexTable
              columnsData={columnsDataComplex}
              tableData={(data as unknown) as TableData[]}
            />
          </SimpleGrid>
          <Card>
            <Text fontSize='xl' fontWeight='400'>
								Prototype Submission and Demonstration for:
							</Text>
              <Image 
              pt='10px'
              borderRadius='20px'
              src="https://race.reva.edu.in/wp-content/uploads/Hackathon_story_banner-4.jpg"></Image>
            </Card> 
        </>
      </Box>
    </AdminLayout>
  )
}
