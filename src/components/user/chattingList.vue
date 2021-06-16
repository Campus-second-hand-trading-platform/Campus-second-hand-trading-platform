<template>
 <div class="container">
   <el-row>
     <el-col :span="12" :offset="3">
       <div class="list">
         <div class="title">
           往来私信
         </div>
         <div @click="toPage('/chatting/to/'+i.userId)" class="list-item" v-for="(i,index) in list1" :key="index">
           <div style="display:inline-block; font-size: 25px"><i class="fa fa-user-circle" aria-hidden="true"></i></div>
           <h3 style="display:inline-block; padding: 5px">{{i.userId}}</h3>
           <p>{{i.chattext}}</p>
         </div>
       </div>
     </el-col>
     <el-col :span="5" :offset="1">
       <div class="tips">
         <h3>规范</h3>
         <span>您可以通过私信和网站的其他人进行秘密沟通。</span>
         <span>沟通的过程中，请保持礼貌。</span>
         <span>禁止故意通过私信传播垃圾广告信息。</span>
       </div>
     </el-col>
   </el-row>
 </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      list1: [
        { userId: '18301082', nickname: 'sds', chattext: 'xxxxx' },
        { userId: '18301085', nickname: 'sdsfeds', chattext: 'xxxxx' }
      ],
      sel1: 1,
      text1: ''
    }
  },
  methods: {
    getChattingList () {
      this.$http.get('/chattinglist', {
        params: {
          userId: sessionStorage.getItem('userId')
        }
      }).then(res => {
        console.log(res.data.data)
        this.list1 = []
        this.list1 = res.data.data
      })
    },
    toPage (page) {
      this.$router.push(page)
    }
  },
  created () {
    this.getChattingList()
  }
}
</script>

<style lang="less" scoped>
  .container{
    margin: 50px 10px;
  }
  .list {
    background-color: #f5f6f7;
  }
  .list .title {
    padding: 15px;
    font-size: 25px;
    border-bottom: 2px solid #ffffff;
  }
  .list .list-item {
    padding: 16px;
    margin: 3px;
    border-bottom: 2px solid #ffffff;
  }
  .list .list-item:hover {
    background-color: #eeeeee;
    cursor: pointer;
  }
  .tips {
    padding: 10px;
    font-size: 13px;
    background-color: #f5f6f7;
  }
  .tips h3 {
    font-size: 15px;
    margin: 8px;
  }
  .tips span {
    display: block;
    margin: 6px;
    color: rgba(0,0,0,.8);
  }
</style>
