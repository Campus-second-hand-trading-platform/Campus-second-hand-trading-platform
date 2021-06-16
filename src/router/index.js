import Vue from 'vue'
import VueRouter from 'vue-router'
// import HelloWorld from '../components/HelloWorld'
import Base from '../components/user/Base'
import Goods from '../components/user/Goods'
import InfoBase from '../components/user/UserInfor/InfoBase'
import Order from '../components/user/UserInfor/Order'
import Index from '../components/user/Index'
import PersonInfo from '../components/user/UserInfor/PersonInfo'
import Login from '../components/user/Login'
import GoodsDetail from '../components/user/GoodsDetail'
import Seek from '../components/user/UserInfor/Seek'
import MySeek from '../components/user/UserInfor/MySeek'
import SeekModify from '../components/user/UserInfor/SeekModify'
import OrderInfo from '../components/user/OrderInfo'
import SellerBase from '../components/user/seller/sellerBase'
import Base2 from '../components/user/seller/base2'
import myGoods from '../components/user/seller/myGoods'
import Order2 from '../components/user/seller/Order2'
import postGoods from '../components/user/seller/postGoods'
import sellerInfo from '../components/user/seller/sellerInfo'
import base3 from '../components/user/manager/base'
import ReportsTable from '../components/user/manager/ReportsTable'
import modifyGoods from '../components/user/seller/modifyGoods'
import ReportsSolve from '../components/user/manager/ReportsSolve'
import SeekPage from '../components/user/SeekPage'
import managerLogin from '../components/user/manager/managerLogin'
import Chatting from '../components/user/Chatting'
import chattingList from '../components/user/chattingList'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/index' },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/manager/login',
    component: managerLogin
  },
  {
    path: '/base2',
    component: Base2,
    children: [
      {
        path: '/seller',
        component: SellerBase,
        children: [
          { path: '/seller/personalInfo', component: sellerInfo },
          { path: '/seller/order', component: Order2 },
          { path: '/seller/postGoods', component: postGoods },
          { path: '/seller/myGoods', component: myGoods },
          { path: '/seller/modifyGoods/:goodsId', component: modifyGoods }
        ]
      }
    ]
  },
  {
    path: '/base',
    component: Base,
    children: [
      { path: '/index', component: Index },
      { path: '/Goods/type/:classID', component: Goods },
      { path: '/Goods/:goodsId', component: GoodsDetail },
      { path: '/order/:orderId', component: OrderInfo },
      { path: '/seeks', component: SeekPage },
      { path: '/chatting/to/:receiver', component: Chatting },
      { path: '/chattingList', component: chattingList },
      {
        path: '/userInfo',
        component: InfoBase,
        children: [
          { path: '/userInfo/order', component: Order },
          { path: '/userInfo/personalInfo', component: PersonInfo },
          { path: '/userInfo/mySeek', component: MySeek },
          { path: '/seek', component: Seek },
          { path: '/userInfo/seekModify/:type/:seekid', component: SeekModify, name: 'seekModify' }
        ]
      }
    ]
  },
  {
    path: '/base3',
    component: base3,
    children: [
      {
        path: '/manager/reports/all',
        component: ReportsTable
      },
      {
        path: '/manager/reports/unsolved',
        component: ReportsSolve
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
