<template>
  <div>
    <!--页头-->
    <div id="headCon">
      <div>
        <p>你的多余 我的需要~</p>
        <ol>
          <a href="#" @click="toPage('index',-1)">切换至买家</a>
        </ol>
      </div>
      <ul>
        <a href="#"><i class="logo fa fa-american-sign-language-interpreting" aria-hidden="true"></i></a>
      </ul>
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
      activePage: 0
    }
  },
  methods: {
    toPage (id, page) {
      this.activePage = page
      sessionStorage.setItem('activePage', page)
      if (id === 'index') {
        this.$router.push('/' + id)
      } else if (id === 'goods') {
        this.$router.push('/goods/' + page)
      } else {
        this.$router.push('/' + id)
      }
    }
  },
  created () {
    this.activePage = sessionStorage.getItem('activePage')
  }
}
</script>

<style scoped>
  @import "~@/assets/css/base.css";
  .search button {
    cursor: pointer;
  }
</style>
