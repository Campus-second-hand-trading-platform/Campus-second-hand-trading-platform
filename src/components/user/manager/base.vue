<template>
  <div class="height">
    <el-container class="container">
      <el-header>
        <div>
          <span class="favicon">校园二手交易</span>
          <span class="title">管理员后台审核系统</span>
        </div>
        <el-button type="info" @click="quitBtnHandle">退出</el-button>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            background-color="#333744"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
          >
            <el-menu-item index="/manager/reports/all">
              <i class="el-icon-reading"></i>
              <span slot="title">所有举报</span>
            </el-menu-item>
            <el-menu-item index="/manager/reports/unsolved">
              <i class="el-icon-reading"></i>
              <span slot="title">举报审核</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: '',
  methods: {
    quitBtnHandle () {
      window.sessionStorage.removeItem('managerId')
      window.sessionStorage.removeItem('mIsLogin')
      this.$router.push('/manager/login')
    }
  }
}
</script>

<style lang="less" scoped>
  .height {
    min-height:730px;
  }
  .height>section {
    height: 730px;
  }
  .container {
    height: 100%;
  }
  .el-header {
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .favicon{
      font-weight: 700;
      font-size: 40px;
      color: #fff;
      text-shadow: 2px 5px 3px rgba(0, 0, 0, 0.06);
      padding: 3px;
    }
    .title {
      color: #ffffff;
      margin-left: 8px;
      font-size: 23px;
    }
  }
  .el-aside {
    background-color: #333744;
  }
  .el-main {
    /*background-color: #eaedfe;*/
    background-color: #f1f2f4;
  }
</style>
