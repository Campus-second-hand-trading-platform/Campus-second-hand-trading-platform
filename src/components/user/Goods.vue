<template>
<div>
  <div class="main" style="margin-top: 50px">
    <el-row>
      <el-col :md="20" :offset="2">
        <div class="content">
          <div style="margin-right: 15px; word-break: break-all">
            <ol type="1">
              <div v-for="(good,index) in this.goods" :key="index" class="box">
                <li style="cursor: pointer" @click="postDetail(good.gid)">
                  <el-card :body-style="{ padding: '0px' }" shadow="hover">
<!--                    <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">-->
                    <img :src="good.picture" class="image" style="width: 196px;height: 196px">
                    <div>
                      <div class="box-title">{{good.gname}}</div>
                      <div class="box-price">¥ {{good.gprice}}</div>
                      <div class="box-seller"><i style="color: #FD3F31; margin-right:7px" class="fa fa-user-circle" aria-hidden="true"></i>{{good.sellerid}}</div>
                    </div>
                  </el-card>
                </li>
              </div>
            </ol>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      classID: this.$route.params.classID,
      goods: [
        {
          id: '1',
          type: '手机',
          title: '2021春夏新款华为5G手机45648946',
          price: 2888.0,
          seller: 'YC',
          pic: require('@/assets/images/use/phone1.jpg')
        }
      ]
    }
  },
  methods: {
    postDetail (goodsId) {
      // this.$router.push('/Goods/' + this.classID + '/' + goodsId)
      this.$router.push('/Goods/' + goodsId)
    },
    getGoods () {
      this.$http.get('goods', {
        params: {
          type: this.classID
        }
      }).then(res => {
        console.log(res.data.data)
        this.goods = res.data.data
        for (var i = 0; i < this.goods.length; i++) {
          // alert(this.goods.length)
          // this.goods[i].picture = '../../../../assets/images/userImg/upload/' + this.goods[i].picture
          this.goods[i].picture = require('@/assets/images/userImg/upload/' + this.goods[i].picture)
        }
      }).catch(err => {
        console.log('获取商品列表失败' + err)
      })
    },
    getGoodsByName () {
      this.$http.get('goods/search', {
        params: {
          searchKey: this.classID
        }
      }).then(res => {
        console.log(res.data.data)
        this.goods = res.data.data
        for (var i = 0; i < this.goods.length; i++) {
          // alert(this.goods.length)
          // this.goods[i].picture = '../../../../assets/images/userImg/upload/' + this.goods[i].picture
          this.goods[i].picture = require('@/assets/images/userImg/upload/' + this.goods[i].picture)
        }
      }).catch(err => {
        console.log('获取商品列表失败' + err)
      })
    }
  },
  mounted () {
    if (this.classID === '1' || this.classID === '2' || this.classID === '3' || this.classID === '4') {
      this.getGoods()
    } else {
      this.getGoodsByName()
    }
  },
  watch: {
    $route (to, from) {
      this.classID = this.$route.params.classID
      if (this.classID === '1' || this.classID === '2' || this.classID === '3' || this.classID === '4') {
        this.getGoods()
      } else {
        this.getGoodsByName()
      }
    }
  }
}
</script>

<style scoped>
  *{
    padding:0;
    margin:0;
    box-sizing:border-box;
  }
  li{
    display:inline
  }
  .content {
    margin-left: 28px;
  }
  .el-card {
    width: 234px;
    height: 336px;
    padding: 22px 18px;
    border: 1px solid #f2f2f2;
    border-radius: 0px;
  }
  .el-card img{
    width: 100%;
  }
  .box {
    display: inline-block;
    margin-right: 10px;
  }
  .box-title {
    min-height: 38.4px;
    margin-top: 10px;
    font-size: 14px;
    color:#9B9B9B;
  }
  .box-price {
    margin-top: 8px;
    color: #FD3F31;
  }
  .box-seller {
    margin-top: 5px;
    font-size: 12px;
    color:#9B9B9B;
  }

</style>
