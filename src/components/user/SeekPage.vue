<template>
  <el-row style="margin-top: 30px">
    <el-col :md="18" :offset="3">
      <div>
        <div></div>
        <!--    所有博客内容-->
        <div class="post-content">
          <h2>所有求购</h2>
          <section v-for="(post,index) in posts" :key="index">
            <h3>标题：{{post.stitle}}</h3>
            <div class="user">
              <i class="el-icon-user"></i>
              <span class="likeNum">{{post.uid}}</span>
            </div>
            <div class="description">
              具体描述：{{post.sdescription}}
            </div>
            <div class="comment">
              <div class="commentBtn">
                <span @click="post.show=!post.show;getComments(post.seekid)"><i class="el-icon-caret-bottom"></i>全部回复</span>
                <div v-show="post.show">
                  <div class="myComment">
                    <el-input v-model="post.commentInput" placeholder="请输入内容" style="width: 500px"></el-input>
                    <el-button @click="postComment(post.seekid)">评论</el-button>
                  </div>
                  <section  v-for="(comment,index) in post.comments" :key="index" >
                    <i class="el-icon-s-custom"></i>
                    <span>{{comment.uid}}:</span>
                    <p>{{comment.commentcontent}}</p>
                  </section>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'blog',
  data () {
    return {
      posts: [
        {
          uid: '18301082',
          seekid: '183010822165',
          stitle: '求购一部华为5G手机,价格可聊',
          sdescription: 'dsdsdsdsdsdsdsdsdsds',
          stime: '2021-06-01',
          show: false,
          commentInput: '',
          comments: [
            {
              uid: 18301082,
              commentcontent: 'sdsdsdssdsdsasssssssssssssssssssss'
            },
            {
              uid: 18301082,
              commentcontent: 'sdsdsdssds'
            }
          ]
        },
        {
          uid: '18301082',
          seekid: '183010822165',
          stitle: '求购一部华为5G手机,价格私聊',
          sdescription: 'dsdsdsd',
          stime: '2021-06-01',
          show: false,
          commentInput: '',
          comments: [
            {
              uid: 18301082,
              commentcontent: 'sdsdsdssds'
            },
            {
              uid: 18301082,
              commentcontent: 'sdsdsdssds'
            }
          ]
        }
      ]
    }
  },
  created () {
    this.getAllseeks()
  },
  methods: {
    getAllseeks () {
      this.$http.get('seeks')
        .then(res => {
          const data = res.data
          console.log(data)
          if (data.stateCode === 200) {
            this.posts = data.data
            for (let i = 0; i < this.posts.length; i++) {
              this.$set(this.posts[i], 'show', false)
              this.$set(this.posts[i], 'commentInput', '')
            }
          }
        }, error => console.log(error))
    },
    getComments (seekid) {
      this.$http.get('/seek/' + seekid + '/comments')
        .then(res => {
          const data = res.data
          console.log(data)
          if (data.stateCode === 200) {
            var index = this.posts.findIndex(function (item) {
              return item.seekid === seekid
            })
            this.$set(this.posts[index], 'comments', data.data)
            // this.posts[index].comments = data.data
          }
        }, error => console.log(error))
    },
    postComment (seekid) {
      var index = this.posts.findIndex(function (item) {
        return item.seekid === seekid
      })
      this.$http.post('/seek/comment', {
        seekId: seekid,
        userId: sessionStorage.getItem('userId'),
        content: this.posts[index].commentInput
      })
        .then(res => {
          const data = res.data
          console.log(data)
          if (data.stateCode === 200) {
            this.$message.success('评价成功')
            this.getComments(seekid)
          }
        }, error => console.log(error))
    }
  }
}
</script>

<style lang="less" scoped>
  .post-content {
    margin-top: 15px;
  }
  h2 {
    margin: 20px 10px;
    font-size:2rem;
    padding: 10px 0;
    border-bottom: 1px dashed #CCCCCC;
  }
  section {
    /*height: 87px;*/
    border-bottom: 1px solid rgba(0,0,0,.1);
    margin: 10px 0;
  }
  h3 {
    font-size: 1.25rem;
    margin: 10px;
    font-weight:normal
  }
  a {
    display: block;
    font-size: 1rem;
    margin: 30px 10px;
  }
  .user {
    display: inline-block;
    margin-left: 10px;
  }
  .description {
    margin: 10px;
    font-size: 16px;
  }
  .myComment {
    margin: 10px;
  }
  .comment {
    background-color: #fafaff;
    padding: 10px;
  }
  .comment>.commentBtn>span:hover {
    cursor: pointer;
  }
  .comment section {
    margin: 10px;
  }
  .comment section span{
    margin: 10px;
  }
  .comment section p{
    margin: 10px;
  }

</style>
