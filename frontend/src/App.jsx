import React from 'react'
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/UserFrontend/HomePage'
import FrontendMain from './pages/UserFrontend/FrontendMain'
import AllCategory from './pages/UserFrontend/AllCategory'
import AllProducts from './pages/UserFrontend/AllProducts'
import AllCategoryProduct from './pages/UserFrontend/AllCategoryProduct'
import SingleProduct from './pages/UserFrontend/SingleProduct'
import CartPage from './pages/UserFrontend/CartPage'
import ContactPage from './pages/UserFrontend/ContactPage'
import LoginPage from './pages/Auths/LoginPage'
import RegisterPage from './pages/Auths/RegisterPage'
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';
import PrivateRoute from './PrivateRoute'
import AddProduct from './pages/Admin/AddProduct'
const queryClient = new QueryClient();

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
        <Routes>
          <Route path='/' element={<FrontendMain />}>
              <Route index element={<HomePage />} />
              <Route path='category' element={<AllCategory />} />
              <Route path='product' element={<AllProducts />} />
              <Route path='singlecategory/:id' element={<AllCategoryProduct />} />
              <Route path='singleProduct/:id' element={<SingleProduct />} />
              <Route path='cart' element={<CartPage />} />
              <Route path='contact' element={<ContactPage />} />

              {/* User Routes */}
              <Route path="/cahangepassword" element={<PrivateRoute allowedRoles={[1]} />}>
                <Route index element={<h1>Change Password</h1>} />
              </Route>
              <Route path="/updateprofile" element={<PrivateRoute allowedRoles={[1]} />}>
                <Route index element={<h1>Update Profile</h1> } />
              </Route>

              {/* Auth */}
              <Route path='login' element={<LoginPage />} />
              <Route path='register' element={<RegisterPage />} />
              {/* Admin Routes  */}
              <Route path="/admin/*" element={<PrivateRoute allowedRoles={[0]} />}>
                <Route index element={<AddProduct />} />
                <Route path="addProduct" element={<AddProduct />} />
              </Route>

          </Route>
      </Routes>
    </QueryClientProvider>
  )
}

export default App
