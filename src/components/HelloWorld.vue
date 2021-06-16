<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <i class="fa fa-camera-retro fa-lg"></i>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: '456'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
  .hello{
    color: pink;
    h1 {
      font-size: 50px;
    }
  }
</style>
