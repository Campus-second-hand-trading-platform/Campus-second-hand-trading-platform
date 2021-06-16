<template>
<div>
  <!--页头-->
  <div id="headCon">
    <div>
      <p>你的多余 我的需要~</p>
    </div>
    <ul>
      <a href="index.html"><i class="logo fa fa-american-sign-language-interpreting" aria-hidden="true"></i></a>
      <span></span>
      <p>{{title}}</p>
    </ul>
  </div>
  <!--内容-登录-->
  <div id="contentCon" v-show="flag==0">
    <div>
      <ul>
        <li>
          <p>{{title}}</p>
<!--          <span>快捷登录</span>-->
        </li>
        <!--      登录表单区域-->
        <div class="login_info" >
          <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
            <el-form-item prop="userId">
              <el-input v-model="loginForm.userId" placeholder="请输入学生ID" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="loginForm.password" placeholder="请输入密码" prefix-icon="el-icon-key" type="password"></el-input>
            </el-form-item>
            <el-form-item class="btns">
              <el-button type="primary" @click="login">登录</el-button>
            </el-form-item>
          </el-form>
          <el-link type="info" @click="registerPage">没有账号？立即注册</el-link>
        </div>
        <!--      注册表单区域-->
        <div class="register_info" v-show="flag==1">
          <el-form :model="registerForm" :rules="rules" ref="registerFormRef">
            <el-form-item prop="userId">
              <el-input v-model="registerForm.userId" placeholder="请输入学生ID" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="nickname">
              <el-input v-model="registerForm.nickname" placeholder="请输入2-15位用户名" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="password1">
              <el-input v-model="registerForm.password1" placeholder="请输入6-20位密码" prefix-icon="el-icon-key" type="password"></el-input>
            </el-form-item>
            <el-form-item prop="password2">
              <el-input v-model="registerForm.password2" placeholder="请重复输入密码" prefix-icon="el-icon-key" type="password"></el-input>
            </el-form-item>
            <el-form-item class="btns">
              <el-button type="primary" @click="register">立即注册</el-button>
            </el-form-item>
          </el-form>
          <el-link type="info" @click="loginPage">已有账号？返回登录</el-link>
        </div>
      </ul>
    </div>
  </div>
  <!--内容-注册-->
  <div id="contentCon1" v-show="flag==1">
    <div>
      <ul>
        <li>
          <p>{{title}}</p>
        </li>
        <!--      注册表单区域-->
        <div class="register_info" >
          <el-form :model="registerForm" :rules="rules" ref="registerFormRef">
            <el-form-item prop="userId">
              <el-input v-model="registerForm.userId" placeholder="请输入学生ID" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="realname">
              <el-input v-model="registerForm.realname" placeholder="请输入真实姓名" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="nickname">
              <el-input v-model="registerForm.nickname" placeholder="请输入2-15位用户名" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="password1">
              <el-input v-model="registerForm.password1" placeholder="请输入6-20位密码" prefix-icon="el-icon-key" type="password"></el-input>
            </el-form-item>
            <el-form-item prop="password2">
              <el-input v-model="registerForm.password2" placeholder="请重复输入密码" prefix-icon="el-icon-key" type="password"></el-input>
            </el-form-item>
            <el-form-item prop="phone">
              <el-input v-model="registerForm.phone" placeholder="请输入手机号" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item>
              <el-select v-model="registerForm.department" placeholder="请选择所属学院">
                <el-option label="软件学院" value="软件学院"></el-option>
                <el-option label="计算机学院" value="计算机学院"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item class="btns">
              <el-button type="primary" @click="register">立即注册</el-button>
            </el-form-item>
          </el-form>
          <el-link type="info" @click="loginPage">已有账号？返回登录</el-link>
        </div>
      </ul>
    </div>
  </div>
  <!--页脚-->
  <div id="footCon">
    <ul>
      <li>
        <div class="tuikuan"></div>
        <span></span>
        <ol>
          <h2>订单完成24h内</h2>
          <p>无条件退款</p>
        </ol>
      </li>
      <li>
        <div class="wuxiu"></div>
        <span></span>
        <ol>
          <h2>7*24小时营业</h2>
          <p>全年无休</p>
        </ol>
      </li>
      <li>
        <div class="baoyou"></div>
        <span></span>
        <ol>
          <h2>满88包邮</h2>
          <p>次日送达</p>
        </ol>
      </li>
    </ul>
    <ol>
      <li>
        <i class="logo fa fa-american-sign-language-interpreting" aria-hidden="true"></i>
        <a href="#">www.bjtu.com</a>
        <div>
          <a href="http://www.weibo.com" class="weibo"></a>
          <a href="http://wx.qq.com" class="weixin"></a>
        </div>
      </li>
      <ul>
        <li class="text01">
          <p>关于我们</p>
          <span></span>
          <a href="#">媒体报道</a>
          <a href="#">知识产权</a>
          <a href="#">加入我们</a>
        </li>
        <li>
          <p>帮助中心</p>
          <span></span>
          <a href="#">购物指南</a>
          <a href="#">订单管理</a>
          <a href="#">常见问题</a>
        </li>
        <li>
          <p>服务支持</p>
          <span></span>
          <a href="#">服务保障</a>
          <a href="#">用户协议</a>
          <a href="#">售后服务</a>
        </li>
        <li>
          <p>商业合作</p>
          <span></span>
          <a href="#">集合采购</a>
          <a href="#">品牌合作</a>
          <a href="#">媒体合作</a>
        </li>
      </ul>
      <div>
        <p>联系我们</p>
        <h2>400-8888-000</h2>
        <span>24小时服务热线</span>
        <a href="#">在线客服</a>
      </div>
    </ol>
    <div></div>
    <li>
      <p>Copyright © 2016 .All Rights Reserved. 北京交通大学软件学院</p>
      <span>版权所有 京ICP备XXX号-1 增值电信业务经营许可证：京ICP证XXX号</span>
    </li>
  </div>
</div>
</template>

<script>
export default {
  name: 'login',
  data () {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.registerForm.password1 !== '') {
          this.$refs.registerFormRef.validateField('password2')
        }
        callback()
      }
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.registerForm.password1) {
        console.log(1)
        callback(new Error('两次输入密码不一致!'))
      } else {
        console.log(value)
        callback()
      }
    }
    return {
      title: '请登录',
      loginForm: {
        userId: '',
        password: ''
      },
      registerForm: {
        nickname: '',
        useId: '',
        realname: '',
        password1: '',
        password2: '',
        phone: '',
        department: ''
      },
      flag: 0,
      rules: {
        userId: [
          { required: true, message: '请输入学生id', trigger: 'blur' },
          { min: 8, max: 8, message: 'id格式错误', trigger: 'blur' }
        ],
        realname: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        nickname: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 2, max: 15, message: '长度在 2 到 15 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        // 自定义检测
        password1: [
          { validator: validatePass, trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        password2: [
          { validator: validatePass2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    reset () {
      console.log(this)
      if (this.flag === 0) { this.$refs.loginFormRef.resetFields() } else {
        this.$refs.registerFormRef.resetFields()
      }
    },
    login () {
      // 方法一  async异步 await 等待
      this.$refs.loginFormRef.validate(async valid => {
        console.log(valid)
        if (!valid) { return }
        const result = await this.$http.post('user/login', this.loginForm)
        console.log(result.data)
        if (result.data.stateCode === 200) {
          sessionStorage.setItem('userId', this.loginForm.userId)
          sessionStorage.setItem('isLogin', true)
          console.log(result.data.message)
          this.$message.success(result.data.message)
          this.$router.push('/index')
        } else if (result.data.stateCode === 202) {
          this.$message.error(result.data.message)
        } else {
          this.$message.error(result.data.message)
        }
      })
    },
    register () {
      this.$refs.registerFormRef.validate(async valid => {
        console.log(valid)
        if (!valid) { return }
        const result = await this.$http.post('user/register', this.registerForm)
        console.log(result.data)
        if (result.data.stateCode === 200) {
          console.log(result.data.message)
          this.$message.success(result.data.message)
          this.flag = 0
        } else if (result.data.stateCode === 202) {
          this.$message.error(result.data.message)
        } else {
          this.$message.error(result.data.message)
        }
      })
    },
    registerPage () {
      this.flag = 1
      this.title = '请注册'
    },
    loginPage () {
      this.flag = 0
      this.title = '请登录'
    },
    stationPage () {
      this.$router.push('/station')
    }
  }
}
</script>

<style lang="less" scoped>
  @import "~@/assets/css/login.scss";
  .el-form-item {
    margin: 30px 0px;
  }
  .el-button {
    width: 100%;
    height: 50px;
    font-size: 20px;
    background-color: #fb0000;
    border: 0px;
  }
  .el-button:hover {
    background-color: #fb423e;
  }

</style>
