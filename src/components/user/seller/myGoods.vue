<template>
  <div>
    <div class="title">
      <ul>
        <li @click="goodsChange(0)" :class="{all:goodsSwitch==0}">我的全部商品</li>
        <li @click="goodsChange(1)" :class="{all:goodsSwitch==1}">待售出</li>
        <li @click="goodsChange(2)" :class="{all:goodsSwitch==2}">已售出</li>
        <li><i class="el-icon-delete" style="font-size: 15px">删除</i></li>
      </ul>
    </div>
    <div class="order-box" v-for="(item,index) in this.goodsShow" :key="index">
      <ol>
        <p v-show="item.gstate===0" style="color: red">已售出</p>
        <p v-show="item.gstate===1" style="color: red">待售出</p>
<!--        <input type="checkbox" :value="item.gid" v-model="deleteOrderList">-->
        <p>商品号：{{item.gid}}</p>
        <p>上架时间：{{item.upload_time}}</p>
        <p>商品名：{{item.gname}}</p>
        <router-link :to="'/seller/modifyGoods/'+item.gid">修改内容</router-link>
<!--        <router-link to="/userInfo/seekModify/1">查看详情</router-link>-->
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      goodsSwitch: 0,
      goodsShow: [],
      goods: [
        {
          gid: 12315,
          gtype: '电子产品',
          gname: '华为5G手机',
          gdescription: 'xxxxxxxxxxxxxxx',
          gprice: 18.99,
          gcount: 1,
          upload_time: '2021-06-01',
          newness: '8成新'
        },
        {
          gid: 12315,
          gtype: '电子产品',
          gname: '华为5G手机',
          gdescription: 'xxxxxxxxxxxxxxx',
          gprice: 18.99,
          gcount: 1,
          upload_time: '2021-06-01',
          newness: '8成新'
        }
      ],
      deleteOrderList: []
    }
  },
  methods: {
    goodsChange (a) {
      this.goodsSwitch = a
      this.goodsShow = []
      if (a === 0) {
        this.goodsShow = this.goods
      } else if (a === 1) {
        this.goods.forEach((good) => {
          if (good.gstate === 1) {
            this.goodsShow.push(good)
          }
        })
      } else if (a === 2) {
        this.goods.forEach((good) => {
          if (good.gstate === 0) {
            this.goodsShow.push(good)
          }
        })
      }
    },
    getMyGoods () {
      this.$http.get('seller/goods', {
        params: {
          userId: sessionStorage.getItem('userId')
        }
      }).then(res => {
        console.log(res.data.data)
        if (res.data.stateCode === 200) {
          this.goods = res.data.data.reverse()
          this.goodsShow = this.goods
        }
      }).catch(err => {
        console.log('获取商品列表失败' + err)
      })
    }
  },
  created () {
    this.getMyGoods()
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
  }
  .title ul>li:hover {
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
    /*background:url(src\assets\images\use\家具1.jpg) no-repeat -687px 0px;*/
    margin-top:18px;
    margin-right:50px;
  }
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
