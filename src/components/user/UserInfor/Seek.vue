<template>
<div>
  <ul class="title">
    <p>发布求购</p>
    <span></span>
  </ul>
  <div class="form">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="标题">
        <el-input v-model="form.stitle"></el-input>
      </el-form-item>
<!--      <el-form-item label="类型">-->
<!--        <el-input v-model="form.type"></el-input>-->
<!--      </el-form-item>-->
      <el-form-item label="仔细描述">
        <el-input type="textarea" :rows="3" v-model="form.sdescription"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即发布</el-button>
        <el-button @click="reset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      resetForm: {},
      form: {
        stitle: '180',
        sdescription: '男',
        type: 'false',
        userId: sessionStorage.getItem('userId')
      }
    }
  },
  methods: {
    onSubmit () {
      this.$http.post('/seek', this.form).then(res => {
        if (res.data.stateCode === 200) {
          this.$message.success(res.data.message)
        }
      })
    },
    reset () {
      this.form = JSON.parse(JSON.stringify(this.resetForm))
    }
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
