<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/base' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>所有举报</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
      <!-- 表格显示区域-->
      <el-table :data="tableData" style="width: 100%"  :default-sort = "{prop: 'state', order: 'descending'}">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="reportid" label="举报ID" width="140"></el-table-column>
        <el-table-column prop="uid" label="举报者用户ID" width="140"></el-table-column>
        <el-table-column prop="gid" label="商品ID" width="140"></el-table-column>
        <el-table-column prop="rtime" sortable label="举报时间" width="170"></el-table-column>
        <el-table-column prop="rreason" label="举报理由" width="250" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-tooltip class="item" effect="dark" content="查看举报内容" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-s-comment" size="mini" @click="checkHandle(scope.row)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!--对话框区域-->
      <el-dialog title="查看举报内容" :visible.sync="checkDialogVisible" width="50%">
        <div>
          <el-form  label-position="right" label-width="70px" ref="formRef" :model="diagForm" >
            <el-form-item label="举报ID" >
              <el-input v-model="diagForm.reportid" disabled></el-input>
            </el-form-item>
            <el-form-item label="举报者ID" >
              <el-input v-model="diagForm.uid" disabled></el-input>
            </el-form-item>
            <el-form-item label="商品ID" >
              <el-input v-model="diagForm.gid" disabled></el-input>
            </el-form-item>
            <el-form-item label="商品链接" >
              <router-link tag="a" target="_blank" :to="/Goods/+diagForm.gid">点击此链接跳转至被举报商品信息</router-link>
            </el-form-item>
            <el-form-item label="举报时间" >
              <el-input v-model="diagForm.rtime" disabled></el-input>
            </el-form-item>
            <el-form-item label="理由" >
              <el-input type="textarea" v-model="diagForm.rreason" disabled></el-input>
            </el-form-item>
          </el-form>
        </div>
        <span slot="footer" class="dialog-footer">
        <el-button @click="checkDialogVisible = false">关闭</el-button>
        </span>
      </el-dialog>
      <el-dialog title="提示" :visible.sync="successDialogVisible" width="50%">
        <span>你确定要通过该项举报吗？</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="successDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="successSubmit">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog title="提示" :visible.sync="unsuccessDialogVisible" width="50%">
        <span>你确定不通过该项举报吗？</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="unsuccessDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="unsuccessSubmit">确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      checkDialogVisible: false,
      successDialogVisible: false,
      unsuccessDialogVisible: false,
      tableData: [
        {
          reportid: '12315',
          uid: '123',
          gid: '15',
          rtime: '2020-10-01',
          rreason: 'xxxxxxxxxxxxx      xxxxxxxxxxxxxxxxx'
        },
        {
          reportid: '12315',
          uid: '123',
          gid: '15',
          rtime: '2020-10-01',
          rreason: 'xxxxxxxxxxxxx'
        }
      ],
      diagForm: {
        reportid: '12315',
        uid: '123',
        gid: '15',
        rtime: '2020-10-01',
        rreason: 'xxxxxxxxxxxxx'
      }
    }
  },
  methods: {
    async successSubmit () {
      const result = await this.$http.put('report/' + this.diagForm.reportid + '/result', { type: 1 })
      console.log(result)
      if (result.data.stateCode === 200) {
        this.$message.success(result.data.msg)
      } else {
        this.$message.error('失败')
      }
      this.successDialogVisible = false
    },
    async unsuccessSubmit () {
      const result = await this.$http.put('report/' + this.diagForm.reportid + '/result', { type: 2 })
      console.log(result)
      if (result.data.stateCode === 200) {
        this.$message.success(result.data.msg)
      } else {
        this.$message.error('失败')
      }
      this.unsuccessDialogVisible = false
    },
    unsuccessHandle (data) {
      console.log(data)
      this.diagForm = data
      this.unsuccessDialogVisible = true
    },
    checkHandle (data) {
      console.log(data)
      this.diagForm = data
      this.checkDialogVisible = true
    },
    successHandle (data) {
      console.log(data)
      this.diagForm = data
      this.successDialogVisible = true
    }
  },
  created () {
    this.$http.get('reports')
      .then(res => {
        console.log(res)
        if (res.data.stateCode === 200) {
          this.tableData = res.data.data
        }
      }, error => console.log(error))
  }
}
</script>

<style lang="less" scoped>
  .el-breadcrumb {
    font-size: 18px;
    margin-bottom: 15px;
  }
  .el-card {
    box-shadow: 0 1px 1px rgba(0,0,0,0.15);
  }
</style>
