<template>
  <div>
    <ul class="title">
      <p>发布商品</p>
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
            <el-option label="电子产品" value=1></el-option>
            <el-option label="图书" value=2></el-option>
            <el-option label="生活用品" value=3></el-option>
            <el-option label="其他用品" value=4></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成色" >
          <el-input v-model="form.newness" style="width: 100px" placeholder="请输入数字"></el-input><span style="margin-left: 10px">成新</span>
        </el-form-item>
        <el-form-item label="仔细描述">
          <el-input type="textarea" :rows="3" v-model="form.gdescription" placeholder="请输入对商品的详细描述"></el-input>
        </el-form-item>
        <el-form-item label="图片上传">
          <el-upload
            class="upload-demo"
            action="http://localhost:9000/up_photo"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
            :on-success="handle_success"
            :limit="1"
            list-type="picture">
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
          </el-upload>
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
      fileList: [
        // {
        //   name: 'food.jpeg',
        //   url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        // },
        // {
        //   name: 'food2.jpeg',
        //   url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        // }
      ],
      resetForm: {},
      form: {
        gname: '诺基亚',
        gprice: '19.9',
        sellerid: sessionStorage.getItem('userId'),
        gtype: '1',
        gdescription: '砸核桃专用',
        newness: 10,
        picture: 123
      }
    }
  },
  methods: {
    async onSubmit () {
      console.log('submit!')
      const result = await this.$http.post('goods', this.form)
      console.log(result)
      console.log(result.data.stateCode === 200)
      if (result.data.stateCode === 200) {
        this.$message.success(result.data.message)
      } else {
        this.$message.error('发布失败')
      }
    },
    reset () {
      this.form = JSON.parse(JSON.stringify(this.resetForm))
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
      alert(1)
    },
    handlePreview (file) {
      console.log(file)
    },
    handle_success (res, file, fileList) {
      console.log(file)
      // this.form.picture = file.url
      this.form.picture = res.path
      // console.log(fileList)
      this.$message.success('图片上传成功')
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
