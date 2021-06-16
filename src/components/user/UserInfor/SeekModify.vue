<template>
  <div>
    <ul class="title">
      <p>{{title}}</p>
      <span></span>
    </ul>
    <div class="form">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="求购号" >
          <el-input v-model="form.seekid" disabled></el-input>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="form.stitle" :disabled="type==1"></el-input>
        </el-form-item>
<!--        <el-form-item label="类型">-->
<!--          <el-input v-model="form.type" :disabled="type==1"></el-input>-->
<!--        </el-form-item>-->
        <el-form-item label="仔细描述">
          <el-input type="textarea" :rows="3" v-model="form.sdescription" :disabled="type==1"></el-input>
        </el-form-item>
        <el-form-item v-show="type==2">
          <el-button type="primary" @click="onSubmit">立即保存</el-button>
          <el-button >取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      type: this.$route.params.type,
      seekid: this.$route.params.seekid,
      title: this.$route.params.type === '1' ? '求购信息' : '修改求购',
      form: {
        seekid: '1801264',
        stitle: '180',
        sdescription: '男',
        type: 'false',
        userId: sessionStorage.getItem('userId')
      }
    }
  },
  methods: {
    onSubmit () {
      console.log('submit!')
      this.$http.put('seek/' + this.seekid, this.form).then(res => {
        console.log(res.data.data)
        if (res.data.stateCode === 200) {
          this.form = res.data.data
          this.$message.success('修改信息成功')
        }
      }).catch(err => {
        console.log('获取指定求购失败' + err)
      })
    },
    reset () {
      this.form = JSON.parse(JSON.stringify(this.resetForm))
    },
    getSeeks () {
      this.$http.get('seek/' + this.seekid).then(res => {
        console.log(res.data.data)
        this.form = res.data.data
      }).catch(err => {
        console.log('获取指定求购失败' + err)
      })
    }
  },
  created () {
    this.getSeeks()
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
