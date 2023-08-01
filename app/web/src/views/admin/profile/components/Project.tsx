// Chakra imports
import {
  Box,
  Flex,
  Icon,
  Link,
  Text,
  useColorModeValue
} from '@chakra-ui/react'
// Custom components
import Card from 'components/card/Card'
import { Image } from 'components/image/Image'
// Assets
import { MdEdit } from 'react-icons/md'

export default function Project (props: {
  title: string
  ranking: number | string
  link: string
  image: string
  [x: string]: any
}) {
  const { title, ranking, link, image, ...rest } = props
  // Chakra Color Mode
  const textColorPrimary = useColorModeValue('secondaryGray.900', 'white')
  const textColorSecondary = 'gray.400'
  const brandColor = useColorModeValue('brand.500', 'white')
  const bg = useColorModeValue('white', 'navy.700')
  return (
<></>
  )
}
