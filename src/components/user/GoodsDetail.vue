<template>
  <div id="contentCon">
    <ul>
      <li>{{goods.gname}}</li>
      <li class="right">
        <a href="#" @click="dialogFormVisible = true"><i style="margin-right: 10px" class="fa fa-flag-o" aria-hidden="true"></i>举报</a>

        <el-dialog title="举报内容" :visible.sync="dialogFormVisible">
          <el-form :model="report">
            <el-form-item label="举报理由" label-width="120px">
              <el-input v-model="report.reason" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="reportSubmit">确 定</el-button>
          </div>
        </el-dialog>
      </li>
    </ul>
    <div id="show">
      <div>
<!--        <ol><img :src="goods.pic[0]" alt=""></ol>-->
      <ol><img :src="goods.pic" alt=""></ol>
      </div>
      <div class="right">
        <p>{{goods.gname}}</p>
        <div>
          <ul>
            <span>¥</span>
            <h2>{{goods.gprice}}</h2>
<!--            <p>（降价通知）</p>-->
          </ul>
<!--          <ol>-->
<!--            <a href="#" class="tehui">特惠</a>-->
<!--            <a href="#">领取满150减15元券，先到先得</a>-->
<!--          </ol>-->
          <li>
            <p>服务</p>
            <div>
              <span>.</span>
              <p>7*24h营业</p>
              <span>.</span>
              <p>不支持无理由退货</p>
              <span>.</span>
              <p>24小时极速退款</p>
            </div>
          </li>
        </div>
        <ul>
          <li class="check01">
            <p>类型</p>
            <span>{{goods.gtype}}</span>
          </li>
          <ol>
            <p>上架时间</p>
            <span>{{goods.upload_time}}</span>
          </ol>
          <ol>
            <p>卖家</p>
            <span>{{goods.sellername}}</span>
          </ol>
          <ol>
            <p>成色</p>
            <span>{{goods.newness}}成新</span>
          </ol>
          <a @click="buy" href="#" class="buy">立刻购买</a>
          <a href="#" class="car" @click="toPage('/chatting/to/'+goods.sellerid)">聊聊</a>
<!--          <a href="#" class="love"></a>-->
        </ul>
      </div>
    </div>
    <div id="details">
      <ul>
        <div>
          <p>Details</p>
          <span></span>
        </div>
        <p>卖家自述</p>
        <span></span>
      </ul>
      <ol>
        <div>
<!--          <span>配料</span>-->
<!--          <p>小麦粉，白砂糖，起酥油，人造奶油，鸡蛋，核桃仁，卡士达粉（白砂糖-->
<!--            ，起酥油，奶粉，<br>乙酰化二淀粉磷酸酯，食用香精，β-胡萝卜素），红茶，食用盐，食品添加剂（复配膨<br>-->
<!--            松剂（碳酸氢钠，焦磷酸二氢二钠，磷酸氢钙，玉米淀粉）碳酸氢钠，碳酸氢铵），液体<br>-->
<!--            调味料（水，糯米，大米，柠檬汁）</p>-->
          <p>{{goods.gdescription}}</p>
        </div>
      </ol>
    </div>
    <div id="origin">
      <ul>
        <div>
          <p>Origin</p>
          <span></span>
        </div>
        <p>商品图集</p>
        <span></span>
      </ul>
      <ol>
<!--        <li v-for="(good,index) in this.goods.pic" :key="index"><img :src="good" alt=""></li>-->
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      goods: {
        gid: this.$route.params.goodsId,
        gname: '华为5G手机',
        seller: '1830',
        gprice: '1999.99',
        gtype: '手机',
        gdescription: 'balabalabalaxxxxxxxxxxxxxxxxxxxxxx',
        upload_time: '2021-05-26',
        newness: '8成新',
        pic: [
          require('@/assets/images/use/phone2.jpg'),
          require('@/assets/images/use/手机1.jpg'),
          require('@/assets/images/use/手机2.jpg'),
          require('@/assets/images/use/手机3.jpg')
        ]
      },
      dialogFormVisible: false,
      report: {
        userId: '180',
        reason: ''
      }
    }
  },
  methods: {
    toPage (page) {
      this.$router.push(page)
    },
    open () {
      this.$prompt('请输入举报理由', '举报', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputErrorMessage: '内容不能为空'
      }).then(({ value }) => {
        this.report.reason = value
        if (this.reportSubmit()) {
          this.$message({
            type: 'success',
            message: '举报成功: '
          })
        } else {
          this.$message({
            type: 'error',
            message: '举报失败: '
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消'
        })
      })
    },
    buy () {
      console.log(sessionStorage.getItem('userId'))
      this.$http.post('/orders', {
        gid: this.goods.gid,
        buyerid: sessionStorage.getItem('userId')
      }).then(response => {
        console.log(response.data)
        if (response.data.stateCode === 200) {
          console.log(response.data.data.orderid)
          this.$router.push('/order/' + response.data.data.orderid)
        } else {
          this.$message.error(response.data.message)
        }
      }).catch(error => {
        console.log(error)
      })
    },
    getGoods () {
      this.$http.get('goods/' + this.goods.gid).then(res => {
        console.log(res.data.data)
        this.goods = res.data.data
        this.goods.pic = require('@/assets/images/userImg/upload/' + res.data.data.picture)
      }).catch(err => {
        console.log('获取商品列表失败' + err)
      })
      // return this.$http.get('goods/' + this.goods.gid)
    },
    getUserInfo () {
      this.$http.get('user/information', {
        params: {
          userId: this.goods.sellerid
        }
      }).then(res => {
        console.log(res.data.data)
        this.goods.sellername = res.data.data.nickname
      }).catch(err => {
        console.log('获取信息失败' + err)
      })
      // return this.$http.get('user/information', {
      //   params: {
      //     userId: this.goods.sellerid
      //   }
      // })
    },
    reportSubmit () {
      if (this.report.reason === '') {
        this.$message.error('不能为空')
        return
      }
      this.$http.post('/report', {
        goodsid: this.goods.gid,
        userId: sessionStorage.getItem('userId'),
        reason: this.report.reason
      }).then(res => {
        console.log(res)
        if (res.data.stateCode === 200) {
          this.$message.success('举报成功')
        } else {
          this.$message.error('举报失败')
        }
        this.dialogFormVisible = false
      }).catch(err => {
        console.log(err)
        this.$message.error('举报失败')
      })
    }
  },
  created () {
    this.getGoods()
    // this.$http.all([this.getGoods()])
    //   .then(
    //     this.$http.spread((res1, res2) => {
    //       console.log('全部加载完成')
    //       console.log(res1)
    //       console.log(res2)
    //     })
    //   )
    //   .catch(err => {
    //     console.log(err.response)
    //   })
  }
}
</script>

<style lang="less" scoped>
  @import "~@/assets/css/xiangqing.scss";
</style>
