import {
  Flex,
  Table,
  Progress,
  Icon,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  useColorModeValue
} from '@chakra-ui/react'
import { useMemo } from 'react'
import {
  useGlobalFilter,
  usePagination,
  useSortBy,
  useTable
} from 'react-table'

// Custom components
import Card from 'components/card/Card'
import Menu from 'components/menu/MainMenu'

// Assets
import { MdCheckCircle, MdCancel, MdOutlineError } from 'react-icons/md'
import { TableProps } from '../variables/columnsData'
export default function ColumnsTable(props: TableProps) {
  const { columnsData, tableData, threshold } = props

  const columns = useMemo(() => columnsData, [columnsData])
  const data = useMemo(() => tableData, [tableData])

  const tableInstance = useTable(
    {
      columns,
      data
    },
    useGlobalFilter,
    useSortBy,
    usePagination
  )

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    initialState
  } = tableInstance
  initialState.pageSize = 5

  const textColor = useColorModeValue('secondaryGray.900', 'white')
  const borderColor = useColorModeValue('gray.200', 'whiteAlpha.100')
  return (
    <Card
      flexDirection='column'
      w='100%'
      px='0px'
      overflowX={{ sm: 'scroll', lg: 'hidden' }}
    >
      <Flex px='25px' justify='space-between' mb='10px' align='center'>
        <Text
          fontSize='22px'
          fontWeight='700'
          lineHeight='100%'
        >
          Live View
        </Text>
        <Menu />
      </Flex>
      <Table {...getTableProps()} variant='simple' color='gray.500' mb='24px'>
        <Thead>
          {headerGroups.map((headerGroup, index) => (
            <Tr {...headerGroup.getHeaderGroupProps()} key={index}>
              {headerGroup.headers.map((column, index) => (
                <Th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  pe='10px'
                  key={index}
                  borderColor={borderColor}
                >
                  <Flex
                    justify='space-between'
                    align='center'
                    fontSize={{ sm: '10px', lg: '12px' }}
                  >
                    {column.render('Header')}
                  </Flex>
                </Th>
              ))}
            </Tr>
          ))}
        </Thead>
        <Tbody {...getTableBodyProps()}>
          {page.map((row, index) => {
            prepareRow(row)
            return (
              <Tr {...row.getRowProps()} key={index}>
                {row.cells.map((cell, index) => {
                  let data
                  if (cell.column.Header === 'IMAGE') {
                    data = (
                      <Text fontSize='sm' fontWeight='700'>
                        {cell.value}
                      </Text>
                    )
                  } else if (cell.column.Header === 'DETECTED') {
                    data = (
                      <Flex align='center'>
                        <Icon
                          w='24px'
                          h='24px'
                          me='5px'
                          color={
                            cell.value === 'Yes'
                              ? 'green.500'
                              : cell.value === 'No'
                                ? 'red.500'
                                : cell.value === 'Error'
                                  ? 'orange.500'
                                  : null
                          }
                          as={
                            cell.value === 'Yes'
                              ? MdCheckCircle
                              : cell.value === 'No'
                                ? MdCancel
                                : cell.value === 'Error'
                                  ? MdOutlineError
                                  : null
                          }
                        />
                        <Text fontSize='sm' fontWeight='700'>
                          {cell.value}
                        </Text>
                      </Flex>
                    )
                  } else if (cell.column.Header === 'PREDICTION COUNT') {
                    data = (
                      <Text fontSize='sm' fontWeight='700'>
                        {cell.value}
                      </Text>
                    )
                  } else if (cell.column.Header === 'MAP URL') {
                    data = (
                      <Flex align='center'>
                        {cell.value}
                      </Flex>
                    )
                  } else if (cell.column.Header === 'MAIL SENT') {
                    data = (
                      <Flex align='center'>
                        <Icon
                          w='24px'
                          h='24px'
                          me='5px'
                          color={
                            cell.value > threshold
                              ? 'green.500'
                              : cell.value < threshold
                                ? 'red.500'
                                : cell.value === threshold
                                  ? 'red.500'
                                  : null
                          }
                          as={
                            cell.value > threshold
                              ? MdCheckCircle
                              : cell.value < threshold
                                ? MdCancel
                                : cell.value === threshold
                                  ? MdCancel
                                  : null
                          }
                        />
                        <Text fontSize='sm' fontWeight='700'>
                          Threshold: {threshold}
                        </Text>
                      </Flex>
                    )
                    } else if (cell.column.Header === 'DISTANCE (in km)') {
                      data = (
                        <Text fontSize='sm' fontWeight='700'>
                          {cell.value}
                        </Text>
                      )
                  };

                  return (
                    <Td
                      {...cell.getCellProps()}
                      key={index}
                      fontSize={{ sm: '14px' }}
                      maxH='30px !important'
                      py='8px'
                      minW={{ sm: '150px', md: '200px', lg: 'auto' }}
                      borderColor='transparent'
                    >
                      {data}
                    </Td>
                  )
                })}
              </Tr>
            )
          })}
        </Tbody>
      </Table>
    </Card>
  )
}
