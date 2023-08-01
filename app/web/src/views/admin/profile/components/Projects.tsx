// Chakra imports
import { Text, useColorModeValue } from '@chakra-ui/react'
// Assets
import Project1 from 'img/profile/Project1.png'
import Project2 from 'img/profile/Project2.png'
import Project3 from 'img/profile/Project3.png'
// Custom components
import Card from 'components/card/Card'
import Project from 'views/admin/profile/components/Project'

export default function Projects (props: { [x: string]: any }) {
  const { ...rest } = props
  // Chakra Color Mode
  const textColorPrimary = useColorModeValue('secondaryGray.900', 'white')
  const textColorSecondary = 'gray.400'
  const cardShadow = useColorModeValue(
    '0px 18px 40px rgba(112, 144, 176, 0.12)',
    'unset'
  )
  return (
<></>
  )
}
