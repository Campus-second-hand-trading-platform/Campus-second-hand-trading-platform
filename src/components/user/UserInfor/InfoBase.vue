<template>
<div id="contentCon">
  <div class="left">
    <div></div>
    <p>晨曦夏夜</p>
    <a href="#">切换账号</a>
    <span></span>
    <ul>
      <li><a :class="{my:activePage==0}" @click="toPage('/userInfo/personalInfo',0)" href="#">个人信息</a></li>
      <li><a :class="{my:activePage==1}" @click="toPage('/userInfo/order',1)" href="#">我的订单</a></li>
      <li><a :class="{my:activePage==2}" @click="toPage('/seek',2)" href="#">发布求购</a></li>
      <li><a :class="{my:activePage==3}" @click="toPage('/userInfo/mySeek',3)" href="#">我的求购</a></li>
    </ul>
  </div>
  <div class="right">
    <router-view></router-view>
  </div>
</div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      msg: '132',
      activePage: -1
    }
  },
  methods: {
    toPage (page, num) {
      this.activePage = num
      this.$router.push(page)
    }
  }
}
</script>

<style lang="less" scoped>
  @import "~@/assets/css/userinfo.scss";
</style>
