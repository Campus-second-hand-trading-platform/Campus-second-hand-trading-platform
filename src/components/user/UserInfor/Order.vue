<template>
  <div>
    <div class="title">
      <ul>
        <li @click="ordersChange(0)" :class="{all:ordersSwitch==0}">全部订单</li>
        <li @click="ordersChange(1)" :class="{all:ordersSwitch==1}">待付款</li>
        <li @click="ordersChange(2)" :class="{all:ordersSwitch==2}">待收货</li>
        <li @click="ordersChange(3)" :class="{all:ordersSwitch==3}">已完成</li>
<!--        <li>售后服务</li>-->
        <li><i class="el-icon-delete" style="font-size: 15px">删除</i></li>
      </ul>
    </div>
    <div class="order-box" v-for="(order,index) in this.ordersShow" :key="index">
      <ol>
        <p>2021-5-22&nbsp;&nbsp;&nbsp;&nbsp;订单号：{{order.orderid}}
          <span style="margin-left: 100px;color: #FD3F31" v-show="order.ostate == 2">已退款</span>
        </p>

        <a href="#"></a>
      </ol>
      <div class="order-content">
        <el-row>
          <el-col :md="5">
            <el-image
              style="display: inline-block; width: 150px; height: 150px"
              :src="order.picture"
              >
            </el-image>
          </el-col>
          <el-col :md="5">
            <p>{{order.goodsName}}</p>
            <span><i style="color: #FD3F31; margin-right:7px" class="fa fa-user-circle" aria-hidden="true"></i>{{order.sellerid}}</span>
          </el-col>
          <el-col :md="4">
            <span>¥{{order.price}}</span>
          </el-col>
          <el-col :md="4">
            <span>x1</span>
          </el-col>
          <el-col :md="6">
            <a v-show="order.issent===0" @click="confirm(order.orderid)" href="javascript:void(0)">确认收货</a>
            <a @click="detail(order.orderid)" href="javascript:void(0)">订单详情</a>
            <a @click="drawback(order.orderid)" href="javascript:void(0)" class="text02">退款</a>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      ordersSwitch: 0,
      ordersShow: [],
      orders: [
        {
          id: 12315,
          pic: require('@/assets/images/use/phone1.jpg'),
          seller: '180',
          goodsName: '华为5G手机',
          price: 29.99
        },
        {
          id: 12318,
          pic: require('@/assets/images/use/phone1.jpg'),
          seller: '180',
          goodsName: '华为5G手机',
          price: 29.99
        }
      ],
      deleteOrderList: []
    }
  },
  methods: {
    ordersChange (a) {
      this.ordersSwitch = a
      this.ordersShow = []
      if (a === 0) {
        this.ordersShow = this.orders
      } else if (a === 1) {
        this.orders.forEach((order) => {
          if (order.ostate === 0) {
            this.ordersShow.push(order)
          }
        })
      } else if (a === 2) {
        this.orders.forEach((order) => {
          if (order.issent === 1) {
            this.ordersShow.push(order)
          }
        })
      } else if (a === 3) {
        this.orders.forEach((order) => {
          if (order.confirm === 1) {
            this.ordersShow.push(order)
          }
        })
      }
    },
    async confirm (id) {
      const result = await this.$http.put('/order/deliveryConfirmation', {
        userId: '18301082',
        orderId: id
      })
      // console.log(result)
      if (result.data.stateCode === 200) {
        this.$message.success(result.data.data)
      }
    },
    detail (id) {
      this.$router.push('/order/' + id)
    },
    async drawback (id) {
      const result = await this.$http.get('/order/drawback', {
        params: {
          userId: '18301082',
          orderId: id
        }
      })
      // console.log(result)
      if (result.data.stateCode === 200) {
        this.$message.success('退款成功')
      } else {
        this.$message.error(result.data.data)
      }
    },
    getOrders () {
      this.$http.get('orders/buyer', {
        params: {
          userId: sessionStorage.getItem('userId')
        }
      }).then(res => {
        console.log(res.data.data)
        this.orders = res.data.data.reverse()
        for (var i = 0; i < this.orders.length; i++) {
          this.orders[i].picture = require('@/assets/images/userImg/upload/' + this.orders[i].picture)
        }
        this.ordersShow = this.orders
      }).catch(err => {
        console.log('获取商品列表失败' + err)
      })
    }
  },
  created () {
    this.getOrders()
  }

}
</script>

<style scoped>
  /*头部*/
  .title ul{
    width:924px;
    height:50px;
    overflow:hidden;
    background:#eee;}
  .title ul>li{
    float:left;
    line-height:50px;
    color:#4c4c4c;
    font-size:18px;
    margin-left: 50px;
    cursor: pointer;
  }
  .title ul>li:last-of-type {
    float: right;
    margin-right: 100px;
  }
  .title ul>li:last-of-type:hover {
    cursor: pointer;
  }
  .title ul>.all{
    color:#fb0000;}
  /*订单选框*/
  .order-box ol{
    width:924px;
    height:56px;
    border-top:1px solid #dcdcdc;
    border-bottom:1px solid #dcdcdc;
    margin-top:30px;
    overflow:hidden;
  }
  .order-box >ol>input{
    width:18px;
    height:18px;
    margin-top:20px;
    margin-left:30px;
    float:left;
    outline:none;
  }
  .order-box >ol>p{
    float:left;
    color:#4c4c4c;
    font-size:14px;
    margin-left:14px;
    line-height:58px;}
  .order-box >ol>a{
    float:right;
    width:25px;
    height:25px;
    /*background:url(src\assets\images\use\家具1.jpg) no-repeat -687px 0px;*/
    margin-top:18px;
    margin-right:30px;}
    /*订单内容*/
  .order-content{
    overflow:hidden;
    margin-top:30px;
  }
  .order-content .el-row {
    display: flex;
    align-items: center;
  }
  .order-content .el-col{
    margin: auto;
    text-align:center;
  }
  .order-content .el-col:nth-of-type(2){
    font-size: 14px;
  }
  .order-content .el-col:nth-of-type(2) span{
    display: inline-block;
    color: #999999;
    padding-top: 15px;
  }
  .order-content .el-col:nth-of-type(5) a{
    display: inline-block;
    padding-right: 15px;
  }

</style>
