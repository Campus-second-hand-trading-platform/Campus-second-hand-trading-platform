<template>
  <div class="container">
    <div class="talk_con">
      <div class="talk_show" id="words">
        <div><h3>对话框</h3></div>
        <div :class="[(i.sendId===userId)?'btalk':'atalk']" v-for="(i,index) in list1" :key="index">
          <span>{{i.sendId}}：{{i.chattext}}</span>
        </div>
        <!-- <div class="btalk"><span>B说：还没呢，你呢？</span></div> -->
      </div>
      <div class="talk_input">
        <el-input
          type="textarea"
          :rows="2"
          placeholder="请输入内容"
          v-model="text1"
          style="width: 800px; margin: 10px 20px"
        >
        </el-input>
        <!-- 绑定单击监听,把value传到vue的list1中 -->
        <el-button type="primary" @click="fnAdd" style="float:right; margin: 10px 30px">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      list1: [
        { sendId: '18301082', chattext: '吃饭了吗？' },
        { sendId: '18301085', chattext: '还没呢，你呢？' }
      ],
      userId: '18301082',
      receiveId: '18301085',
      text1: ''
    }
  },
  methods: {
    fnAdd: function () {
      if (this.text1 === '') {
        alert('请输入内容!')
        return
      }
      // 列表追加数据push()
      this.list1.push({ sendId: this.userId, chattext: this.text1 })
      // 每次输入内容后,清空输入栏数据
      this.$http.post('/chatting/send', {
        userId1: this.userId,
        userId2: this.receiveId,
        chattext: this.text1
      })
      this.text1 = ''
    },
    getChattingContent () {
      this.$http.get('/chatting', {
        params: {
          userId1: this.userId,
          userId2: this.receiveId
        }
      }).then(res => {
        console.log(res)
        this.list1 = []
        this.list1 = res.data.data
      })
    }
  },
  created () {
    this.userId = sessionStorage.getItem('userId')
    this.receiveId = this.$route.params.receiver
    this.getChattingContent()
    this.timer = setInterval(() => {
      this.getChattingContent()
    }, 1000 * 5)
  }
}
</script>

<style lang="less" scoped>
.container {
  margin: 20px 160px;
  width: 850px;
  background-color: #f5f6f7;
}
.talk_con {
  /*width: 600px;*/
  /*height: 500px;*/
  /*border: 1px solid #666;*/
  margin: 50px auto 0;
  background: #f5f6f7;
}

.talk_show {
  /*width: 580px;*/
  height: 420px;
  /*border: 1px solid #666;*/
  background: #f5f5f5;
  margin: 10px auto 0;
  overflow: auto;
  border-bottom: 3px solid #ffffff;
}
.talk_show h3 {
  height: 45px;
  font-size: 25px;
  line-height: 45px;
  padding-left: 40px;
  border-bottom: 3px solid #ffffff;
}

.talk_input {
  /*width: 580px;*/
  height: 170px;
  margin: 10px auto 0;
  background-color: #f5f5f5;
}

.whotalk {
  width: 80px;
  height: 30px;
  float: left;
  outline: none;
}

.talk_word {
  width: 420px;
  height: 26px;
  padding: 0px;
  float: left;
  margin-left: 10px;
  outline: none;
  text-indent: 10px;
}

.talk_sub {
  width: 56px;
  height: 30px;
  float: left;
  margin-left: 10px;
}

.atalk {
  margin: 10px;
}

.atalk span {
  display: inline-block;
  background: #0181cc;
  border-radius: 10px;
  color: #fff;
  padding: 5px 10px;
  margin: 5px 15px;
}

.btalk {
  margin: 10px;
  text-align: right;
}

.btalk span {
  display: inline-block;
  background: #ef8201;
  border-radius: 10px;
  color: #fff;
  padding: 5px 10px;
  margin: 5px 15px;
}
</style>
