<template>
  <div>
    <div class="title">
      <ul>
        <li class="all">全部求购</li>
        <li @click="deleteBtn"><i class="el-icon-delete" style="font-size: 15px" >删除</i></li>
      </ul>
    </div>
    <div class="order-box" v-for="(seek,index) in this.seeks" :key="index">
      <ol>
<!--        <input type="checkbox" :value="seek.seekid" v-model="deleteOrderList">-->
        <p>求购号：{{seek.seekid}}</p>
        <p>时间：{{seek.stime}}</p>
        <el-tooltip :content="seek.stitle" placement="top" effect="light">
          <p class="" style="width: 150px;height: 100%; hoverflow: hidden">标题：{{seek.stitle}}</p>
        </el-tooltip>
        <a href="#"><li @click="deleteBtn(seek.seekid)">删除求购</li></a>
        <router-link :to="'/userInfo/seekModify/2/'+seek.seekid">修改内容</router-link>
        <router-link :to="'/userInfo/seekModify/1/'+seek.seekid">查看详情</router-link>

      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      seeks: [
        {
          seekid: '12315',
          stitle: '华为5G手机',
          sdescription: 'xxxxxxxxxxxxxxx',
          stime: '2021-06-01'
        },
        {
          seekid: '12316',
          stitle: '华为5G手机',
          sdescription: 'xxxxxxxxxxxxxxx',
          stime: '2021-06-01'
        }
      ],
      deleteOrderList: []
    }
  },
  methods: {
    deleteBtn (seekid) {
      this.$http.delete('/seek/' + seekid).then(res => {
        this.$message.success('删除成功')
      }).catch(err => {
        console.log(err)
        this.$message.error('删除失败')
      })
    }
  },
  created () {
    this.$http.get('/seek', {
      params: {
        userId: sessionStorage.getItem('userId')
      }
    }).then(res => {
      this.seeks = res.data.data.reverse()
    })
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
    margin-right:30px;
  }
  .order-box >ol>a:first-of-type{
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
