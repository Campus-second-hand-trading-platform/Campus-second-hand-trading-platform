<template>
  <div>
    <div id="contentCon">
      <!-- 轮播图-->
      <el-carousel indicator-position="outside" height="600px">
        <el-carousel-item v-for="(item,index) in boxs" :key="index">
<!--          <div class="box">-->
<!--            <el-row>-->
<!--              <el-col :span="8" :offset="8"><h3>{{item.title}}</h3></el-col>-->
<!--            </el-row>-->
<!--            <el-row>-->
<!--              <el-col :span="8" :offset="8">-->
<!--                <div class="box-content" v-html="item.content">{{item.content}}</div>-->
<!--              </el-col>-->
<!--            </el-row>-->
<!--            <el-row>-->
<!--              <el-col :span="8" :offset="8"> <el-button type="info" round @click="goto(index)">read more</el-button></el-col>-->
<!--            </el-row>-->
<!--          </div>-->
        </el-carousel-item>
      </el-carousel>
      <div class="sell-goods-title">
        <div class="sell-goods-title-h1">昨日我们平台卖出闲置二手价值达</div>
        <div class="sell-goods-title-h2">180189 <span>元</span></div>
      </div>

      <div class="t1">
        <ul>
          <li></li>
          <p>电子产品</p>
          <a href="#">+MORE</a>
        </ul>
        <ol>
          <li class="ice">
            <a href="#"></a>
            <div>华为5G手机</div>
          </li>
          <li class="zhenzi">
            <a href="#"></a>
            <div class="container">
              <a href="western.html" class="dangao"><p>华为原装电脑</p></a>
              <a href="western.html" class="bang"><p>Mac</p></a>
            </div>
          </li>
          <li class="makalong">
            <a href="#"></a>
            <div>iphone</div>
          </li>
        </ol>
      </div>
      <div class="t2">
        <ul>
          <li></li>
          <p>二手图书</p>
          <a href="HongKong.html">+MORE</a>
        </ul>
        <ol>
          <li class="paofu">
            <a href="xiangqing.html">
              <div>
                <span></span>
                <p>文学丛书</p>
              </div>
            </a>
          </li>
          <li>
            <ol>
              <a href="xiangqing.html" class="quqi">
                <div>
                  <p>C<br>语<br>言<br></p>
                </div>
              </a>
              <a href="xiangqing.html" class="paofu">
                <div>
                  <p>文<br>学<br>小<br>说</p>
                </div>
              </a>
              <a href="xiangqing.html" class="niuiaobao">
                <div>
                  <p>数<br>据<br>结<br>构</p>
                </div>
              </a>
            </ol>
            <ol>
              <a href="HongKong.html" class="banji">
                <div>
                  <p>学<br>霸<br>笔<br>记</p>
                </div>
              </a>
              <a href="HongKong.html" class="danta">
                <div>
                  <p>人<br>工<br>智<br>能</p>
                </div>
              </a>
              <a href="HongKong.html" class="moti">
                <div>
                  <p>文<br>学<br>丛<br>书</p>
                </div>
              </a>
            </ol>
          </li>
        </ol>
      </div>
      <div class="t3">
        <ul>
          <li></li>
          <p>生活用品</p>
          <a href="#">+MORE</a>
        </ul>
        <ol>
          <li class="ice">
            <a href="#"></a>
            <div>华为5G手机</div>
          </li>
          <li class="zhenzi">
            <a href="#"></a>
            <div class="container">
              <a href="western.html" class="dangao"><p>华为原装电脑</p></a>
              <a href="western.html" class="bang"><p>Mac</p></a>
            </div>
          </li>
          <li class="makalong">
            <a href="#"></a>
            <div>iphone</div>
          </li>
        </ol>
      </div>

      <div class="jingxuan">
        <ul>
          <p>本月校园活动</p>
          <li></li>
          <span>更换新主人，创造新价值</span>
        </ul>
        <ol>
          <a href="xiangqing.html"><li></li></a>
          <a href="xiangqing.html"><div></div></a>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      boxs: [
        {
          title: '欢迎进入流浪之家',
          content: '<p>寻找你爱的宠物<br>亦或成为志愿者---帮助我们 <br>亦或加入流浪动物圈---分享交流</p>'
        },
        {
          title: '欢迎进入萌宠论坛',
          content: '<p>寻找你爱的宠物<br>亦或成为志愿者---帮助我们 <br>亦或加入流浪动物圈---分享交流</p>'
        },
        {
          title: '联系我们',
          content: '<p>寻找你爱的宠物<br>亦或成为志愿者---帮助我们 <br>亦或加入流浪动物圈---分享交流</p>'
        }
      ]
    }
  }
}
</script>

<style  scoped>
  @import "~@/assets/css/index.css";
  .el-carousel {
    margin-top: 50px;
  }
  /*轮播图*/
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }
  .el-carousel__item:nth-of-type(1) {
    background: url(../../assets/images/use/slide1.jpg) no-repeat center;
    background-size: cover;
  }
  .el-carousel__item:nth-of-type(2) {
    background: url(../../assets/images/use/slide2.jpg) no-repeat center;
    background-size: cover;
  }
  .el-carousel__item:nth-of-type(3) {
    background: url(../../assets/images/use/slide3.jpg) no-repeat center;
    background-size: cover;
  }

  .el-carousel .el-row {
    text-align: center;
    margin: 20px 0;
  }
  .el-carousel .el-row h3 {
    font-size: 48px;
    color: #fff;
    margin: 0 auto;
    text-align: center;
  }
  .el-carousel .el-row .box-content{
    margin-top: -40px;
    font-size: 18px;
    color: #fff;
  }
  .sell-goods-title{
    height: 190px;
    width: 1160px;
    margin: 8px auto 0;
    text-align: center;
    background: url(../../assets/images/sellgoodtitile-bk.png) no-repeat center;
    background-size: 100% 18px;
  }
  .sell-goods-title span{
    font-size: 24px;
  }
  .sell-goods-title .sell-goods-title-h1 {
    padding-top: 60px;
    font-size: 14px;
    color: #200000;
    line-height: 1.3;
    padding-bottom: 2px;
  }
  .sell-goods-title .sell-goods-title-h2 {
    margin-top: 2px;
    font-size: 42px;
    color: #ff5a0c;
    background: #ffffff;
    display: inline-block;
  }

</style>
