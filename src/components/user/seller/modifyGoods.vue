<template>
  <div>
    <ul class="title">
      <p>修改商品</p>
      <span></span>
    </ul>
    <div class="form">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="商品名">
          <el-input v-model="form.gname" style="width: 250px" placeholder="请输入商品名"></el-input>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="form.gprice" style="width: 200px" placeholder="请输入商品价格"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.gtype" placeholder="请选择类型">
            <el-option label="电子产品" value="电子产品"></el-option>
            <el-option label="图书" value="图书"></el-option>
            <el-option label="生活用品" value="生活用品"></el-option>
            <el-option label="其他用品" value="其他产品"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成色" >
          <el-input v-model="form.newness" style="width: 200px" placeholder="请输入成色，例如 “8成新”"></el-input>
        </el-form-item>
        <el-form-item label="是否上架">
          <el-switch v-model="switch1"></el-switch>
        </el-form-item>
        <el-form-item label="仔细描述">
          <el-input type="textarea" :rows="3" v-model="form.gdescription" placeholder="请输入对商品的详细描述"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">立即保存</el-button>
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
      switch1: '',
      form: {
        gname: '',
        gprice: '',
        sellerid: sessionStorage.getItem('userId'),
        gtype: '',
        gdescription: '',
        newness: '',
        gcount: 1
      }
    }
  },
  methods: {
    async onSubmit () {
      console.log('submit!')
      const result = await this.$http.put('goods', this.form)
      console.log(result)
      if (result.data.stateCode === 200) {
        this.$message.success(result.data.message)
      } else {
        this.$message.error('失败')
      }
    },
    reset () {
      this.form = JSON.parse(JSON.stringify(this.resetForm))
    }
  },
  watch: {
    switch1: function (newV, oldV) { // 这个函数一个是输入的新值，一个是原来的值
      console.log(newV, oldV)// 将这两个数值进行打印
      if (newV === false) { // 如果这个新的数值为999就进行打印
        this.form.gcount = 0
      } else {
        this.form.gcount = 1
      }
    }
  },
  created () {
    this.$http.get('goods/' + this.$route.params.goodsId)
      .then(res => {
        console.log(res)
        if (res.data.stateCode === 200) {
          this.form = res.data.data
          if (this.form.gcount === 0) {
            this.switch1 = false
          } else if (this.form.gcount === 1) {
            this.switch1 = true
          }
        }
      }, error => console.log(error))
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
