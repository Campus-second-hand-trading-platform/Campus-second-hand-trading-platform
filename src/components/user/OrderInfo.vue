<template>
  <div class="container">
    <ul class="title">
      <p>订单详情</p>
      <span></span>
    </ul>
    <div class="form">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="订单号">
          <el-input v-model="form.orderid" disabled></el-input>
        </el-form-item>
        <el-form-item label="商品名">
          <el-input v-model="form.gname" disabled></el-input>
        </el-form-item>
        <el-form-item label="买家">
          <el-input v-model="form.buyerName" disabled></el-input>
        </el-form-item>
        <el-form-item label="卖家">
          <el-input v-model="form.sellerName" disabled></el-input>
        </el-form-item>
        <el-form-item label="创建时间" disabled>
          <el-input v-model="form.order_time" disabled></el-input>
        </el-form-item>
        <el-form-item label="价钱" disabled>
          <el-input v-model="form.price" disabled></el-input>
        </el-form-item>

        <el-form-item>
          <el-button :disabled="form.ostate===1" type="primary" @click="onSubmit">立即购买</el-button>
          <el-button @click="cancel">取消订单</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        issent: 1,
        orderid: '18301082120210602153259',
        gid: '18036501',
        gname: '5G手机',
        buyerid: '18301082',
        buyerName: '180',
        sellerName: 'YC',
        order_time: '1999-10-01',
        price: '1000.50'
      }
    }
  },
  methods: {
    onSubmit () {
      console.log('submit!')
      this.$http.put('/orders/buy', {
        orderid: this.form.orderid,
        buyerid: sessionStorage.getItem('userId')
      }).then(response => {
        console.log(response)
        if (response.data.stateCode === 200) {
          this.$message.success(response.data.message)
          this.$router.push('/index')
        } else {
          this.$message.error(response.data.message)
        }
      }).catch(error => {
        console.log(error)
      })
    },
    cancel () {
      console.log('cancel!')
      this.$http.put('/order/cancel', {
        orderId: this.form.orderid,
        userId: sessionStorage.getItem('userId')
      }).then(response => {
        console.log(response)
        if (response.data.stateCode === 200) {
          this.$router.push('/goods/' + this.form.gid)
          this.$message.success(response.data.message)
        } else {
          this.$message.error(response.data.message)
        }
      }).catch(error => {
        console.log(error)
      })
    }
  },
  created () {
    this.$http.get('/orders/' + this.$route.params.orderId).then(response => {
      console.log(response)
      if (response.data.stateCode === 200) {
        this.form = response.data.data
      } else {
        this.$message.error(response.data.message)
      }
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>

<style scoped>
  .container{
    width: 900px;
    margin: 50px auto;
  }
  .title {
    overflow: hidden;
  }
  .title p{
    text-align:center;
    float:left;
    width:112px;
    height:34px;
    font-size:18px;
    border-bottom:1px solid #d2d2d2;
    border-right:1px solid #d2d2d2;
    color:#fb0000;}
  .title span{
    float:left;
    width:762px;
    height:1px;
    background:#d2d2d2;
  }
  .form {
    margin-top: 25px;
  }
</style>
