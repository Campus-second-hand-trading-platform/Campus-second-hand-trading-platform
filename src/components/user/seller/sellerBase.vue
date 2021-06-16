<template>
  <div>
    <div id="contentCon">
      <div class="left">
        <div></div>
        <p>晨曦夏夜</p>
        <a href="#">切换账号</a>
        <span></span>
        <ul>
          <li><a :class="{my:activePage==0}" @click="toPage('/seller/personalInfo',0)" href="#">个人信息</a></li>
          <li><a :class="{my:activePage==1}" @click="toPage('/seller/order',1)" href="#">我的售出</a></li>
          <li><a :class="{my:activePage==2}" @click="toPage('/seller/postGoods',2)" href="#">发布商品</a></li>
          <li><a :class="{my:activePage==3}" @click="toPage('/seller/myGoods',3)" href="#">我的商品</a></li>
        </ul>
      </div>
      <div class="right">
        <router-view></router-view>
      </div>
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
