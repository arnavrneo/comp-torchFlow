// Chakra imports
import { Box, Flex, Text, useColorModeValue } from '@chakra-ui/react'
import Card from 'components/card/Card'
import { NextAvatar } from 'components/image/Avatar'

export default function Banner (props: {
  banner: string
  avatar: string
  name: string
  job: string
  posts: number | string
  followers: number | string
  following: number | string
  [x: string]: any
}) {
  const {
    banner,
    avatar,
    name,
    job,
    posts,
    followers,
    following,
    ...rest
  } = props
  // Chakra Color Mode
  const textColorPrimary = useColorModeValue('secondaryGray.900', 'white')
  const textColorSecondary = 'gray.400'
  const borderColor = useColorModeValue(
    'white !important',
    '#111C44 !important'
  )
  return (
    <></>
  )
}
