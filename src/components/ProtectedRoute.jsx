import { Navigate } from 'react-router-dom'
import { getToken } from '../api/client'

export default function ProtectedRoute({ children }) {
  // TODO: re-enable auth check before production
  // if (!getToken()) {
  //   return <Navigate to="/signin" replace />
  // }
  return children
}
