<template>
<div>
  <!--页头-->
  <div id="headCon">
    <div>
      <p>你的多余 我的需要~</p>
      <ol>
        <li v-show="isLogin==false"><a @click="toPage('login',-1)" href="#">请登录</a></li>
<!--        <li><a href="#">注册</a></li>-->
        <li><a href="#" v-show="isLogin">用户：{{this.userId}}</a></li>
        <a href="#" @click="toPage('userInfo/order',-1)">我的订单</a>
        <a href="#" @click="toPage('userInfo/personalInfo',-1)">个人信息</a>
        <a href="#" @click="toPage('seek',-1)">求购</a>
        <a href="#" @click="toPage('seller',-1)">切换至卖家</a>
        <a href="#" v-show="isLogin" @click="logout">退出</a>
<!--        <a href="shoppingCar.html" class="shoppingCar">-->
<!--          <i></i>-->
<!--          <span>购物车（0）</span>-->
<!--        </a>-->
      </ol>
    </div>
    <ul>
      <a href="#"><i class="logo fa fa-american-sign-language-interpreting" aria-hidden="true"></i></a>
      <ol>
        <li><a :class="{first:activePage==0}" @click="toPage('index',0)" href="#">首页</a></li>
        <li><a :class="{first:activePage==1}" @click="toPage('goods',1)" href="#">电子产品</a></li>
        <li><a :class="{first:activePage==2}" @click="toPage('goods',2)" href="#">图书</a></li>
        <li><a :class="{first:activePage==3}" @click="toPage('goods',3)" href="#">生活用品</a></li>
        <li><a :class="{first:activePage==4}" @click="toPage('goods',4)" href="#">更多品类</a></li>
        <li><a :class="{first:activePage==5}" @click="toPage('seeks',5)" href="#">大家的求购</a></li>
        <li class="search">
          <input v-model="searchKey" placeholder="搜索相关商品"><button @click="toPage('goods',searchKey)"></button>
        </li>
      </ol>
    </ul>
<!--    <div class="flicker-example" data-block-text="false">-->
<!--      <ul>-->
<!--        <li data-background="images/banner_02.jpg">-->

<!--        </li>-->
<!--        <li data-background="images/banner3.jpg">-->

<!--        </li>-->
<!--        <li data-background="images/banner05.png">-->

<!--        </li>-->
<!--      </ul>-->
<!--    </div>-->
  </div>
  <div id="contentCon">
    <router-view></router-view>
  </div>
  <!--页脚-->
  <div id="footCon">
    <ul>
      <li>
        <div class="tuikuan"></div>
        <span></span>
        <ol>
          <h2>订单完成24h内</h2>
          <p>无条件退款</p>
        </ol>
      </li>
      <li>
        <div class="wuxiu"></div>
        <span></span>
        <ol>
          <h2>7*24小时营业</h2>
          <p>全年无休</p>
        </ol>
      </li>
      <li>
        <div class="baoyou"></div>
        <span></span>
        <ol>
          <h2>满88包邮</h2>
          <p>次日送达</p>
        </ol>
      </li>
    </ul>
    <ol>
      <li>
        <i class="logo fa fa-american-sign-language-interpreting" aria-hidden="true"></i>
        <a href="#">www.bjtu.com</a>
        <div>
          <a href="http://www.weibo.com" class="weibo"></a>
          <a href="http://wx.qq.com" class="weixin"></a>
        </div>
      </li>
      <ul>
        <li class="text01">
          <p>关于我们</p>
          <span></span>
          <a href="#">媒体报道</a>
          <a href="#">知识产权</a>
          <a href="#">加入我们</a>
        </li>
        <li>
          <p>帮助中心</p>
          <span></span>
          <a href="#">购物指南</a>
          <a href="#">订单管理</a>
          <a href="#">常见问题</a>
        </li>
        <li>
          <p>服务支持</p>
          <span></span>
          <a href="#">服务保障</a>
          <a href="#">用户协议</a>
          <a href="#">售后服务</a>
        </li>
        <li>
          <p>商业合作</p>
          <span></span>
          <a href="#">集合采购</a>
          <a href="#">品牌合作</a>
          <a href="#">媒体合作</a>
        </li>
      </ul>
      <div>
        <p>联系我们</p>
        <h2>400-8888-000</h2>
        <span>24小时服务热线</span>
        <a href="#">在线客服</a>
      </div>
    </ol>
    <div></div>
    <li>
      <p>Copyright © 2016 .All Rights Reserved. 北京交通大学软件学院</p>
      <span>版权所有 京ICP备XXX号-1 增值电信业务经营许可证：京ICP证XXX号</span>
    </li>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'base',
      searchKey: '',
      activePage: 0,
      isLogin: false,
      userId: sessionStorage.getItem('userId')
    }
  },
  methods: {
    toPage (id, page) {
      this.activePage = page
      sessionStorage.setItem('activePage', page)
      if (id === 'index') {
        this.$router.push('/' + id)
      } else if (id === 'goods') {
        this.$router.push('/goods/type/' + page)
      } else {
        this.$router.push('/' + id)
      }
    },
    logout () {
      sessionStorage.removeItem('userId')
      sessionStorage.removeItem('isLogin')
      this.isLogin = false
    }
  },
  created () {
    this.activePage = sessionStorage.getItem('activePage')
    this.isLogin = sessionStorage.getItem('isLogin')
    if (this.isLogin == null) { this.isLogin = false }
  }
}
</script>

<style scoped>
@import "~@/assets/css/base.css";
  .search button {
    cursor: pointer;
  }
</style>
