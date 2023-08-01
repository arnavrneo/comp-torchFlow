import { Icon } from '@chakra-ui/react'
import {
  MdHome,
  MdLock,
} from 'react-icons/md'

// Admin Imports
import MainDashboard from 'pages/admin/default'

// Auth Imports
import SignInCentered from 'pages/auth/sign-in'
import { IRoute } from 'types/navigation'

const routes: IRoute[] = [
  {
    name: 'Main Dashboard',
    layout: '/admin',
    path: '/default',
    icon: <Icon as={MdHome} width='20px' height='20px' color='inherit' />,
    component: MainDashboard
  },
  {
    name: 'Sign In',
    layout: '/auth',
    path: '/sign-in',
    icon: <Icon as={MdLock} width='20px' height='20px' color='inherit' />,
    component: SignInCentered
  },
]

export default routes
