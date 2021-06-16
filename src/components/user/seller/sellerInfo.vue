<template>
  <div>
    <ul class="title">
      <p>基本资料</p>
      <span></span>
    </ul>
    <div class="form">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="用户昵称">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="学生ID">
          <el-input v-model="form.userId" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.realname" disabled></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.userPhone"></el-input>
        </el-form-item>
        <!--        <el-form-item label="性别">-->
        <!--          <el-select v-model="form.gender" placeholder="请选择性别">-->
        <!--            <el-option label="男" value="男"></el-option>-->
        <!--            <el-option label="女" value="女"></el-option>-->
        <!--          </el-select>-->
        <!--        </el-form-item>-->
        <el-form-item label="所属学院">
          <el-select v-model="form.department" placeholder="请选择学院">
            <el-option label="软件学院" value="软件学院"></el-option>
            <el-option label="计算机学院" value="计算机学院"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="个性签名">
          <el-input type="textarea" v-model="form.signature"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">立即保存</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        username: '180',
        userId: '18301082',
        realname: '王昱',
        phone: '17857242620',
        // headPortrait: require('@/assets/images/use/其他2.jpg'),
        signature: 'false',
        department: '软件学院'
      }
    }
  },
  methods: {
    onSubmit () {
      console.log('submit!')
      this.$http.put('user/information', this.form).then(res => {
        console.log(res.data.data)
        this.$message.success(res.data.message)
      }).catch(err => {
        console.log('修改信息失败' + err)
      })
    },
    getPersonInfo () {
      this.$http.get('user/information', {
        params: {
          userId: sessionStorage.getItem('userId')
        }
      }).then(res => {
        console.log(res.data.data)
        this.form = res.data.data
      }).catch(err => {
        console.log('获取指定求购失败' + err)
      })
    }
  },
  created () {
    this.getPersonInfo()
  }
}
</script>

<style scoped>
  .title {
    overflow: hidden;
  }
  .title p{
    text-align:center;
    float:left;
    width:112px;
    height:34px;
    font-size:18px;
    border-bottom:1px solid #d2d2d2;
    border-right:1px solid #d2d2d2;
    color:#fb0000;}
  .title span{
    float:left;
    width:762px;
    height:1px;
    background:#d2d2d2;
  }
  .form {
    margin-top: 25px;
  }
</style>
