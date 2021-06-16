<template>
  <div id="app">
    <router-view></router-view>
    <div class="aside-bar">
      <div class="bar-item" @click="toPage('/userinfo')"><i class="fa fa-user-o" aria-hidden="true"></i></div>
      <div class="bar-item" @click="toPage('/chattingList')"><i class="fa fa-envelope-o" aria-hidden="true"></i></div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'app',
  methods: {
    toPage (page) {
      console.log(sessionStorage.getItem('isLogin'))
      if (sessionStorage.getItem('isLogin') === 'true') { this.$router.push(page) } else { this.$message.info('请先登录') }
    }
  }
}
</script>

<style>
  .aside-bar {
    position: fixed;
    font-size: 30px;
    bottom: 40%;
    right: 30px;
    z-index: 99;
    border: none;
    outline: none;
    background-color: #9F9F9F;
    color: white;
    cursor: pointer;
    padding: 0 5px;
    border-radius: 2px;
  }
  .bar-item {
    border-bottom: 1px solid #ffffff;
    padding: 5px 0;
  }
  .bar-item:last-of-type {
    border-bottom: 0px solid #ffffff;
  }
</style>
