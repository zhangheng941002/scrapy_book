<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
// import axios from "axios";

export default {
  name: "app",
  components: {},
  data() {
    return {};
  },
  created(){
    if (sessionStorage.getItem("store") ) {
      //页面刷新之后移除session 并重新挂载路由
      this.$store.replaceState(Object.assign({}, this.$store.state,JSON.parse(sessionStorage.getItem("store"))));
      sessionStorage.removeItem("store");
    }

    //监听页面刷新前 vuex 存储
    window.addEventListener("beforeunload",()=>{
      sessionStorage.setItem("store",JSON.stringify(this.$store.state))
    })
  },

  mounted() {
    // this.getMethodData();
  },
  methods: {
    // getMethodData() {
    //   axios
    //     .get("/getApi/other/test_api", {
    //       params: {
    //         username: "admin",
    //         password: "123456",
    //       },
    //     })
    //     .then((data) => {
    //       this.bookTypeList = data.data.data.map((item) => {
    //         let a = {
    //           name: Object.keys(item)[0],
    //           value: Object.values(item)[0],
    //         };
    //         return a;
    //       });
    //       console.log(this.bookTypeList);
    //       this.status = data.data.status;
    //     });
    // },
  },
};
</script>

<style>
html {
  overflow:hidden;
  height:100%;
  font-weight: normal;
  color: #000;
  background: #F1F1F1;
}
body {
  margin:0;
  padding:0;
  font-size:12px;
  height:100%;
  color: #303133;
  overflow-x: auto;
}
div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,form,fieldset,input,textarea,blockquote,p{padding:0; margin:0;outline: none}
table,td,tr,th{font-size:14px;}
li{list-style-type:none;}
img{vertical-align:top;border:0;}
ol,ul {list-style:none;
  margin:0;
  padding:0;}
h1,h2,h3,h4,h5,h6{font-size:12px; font-weight:normal;}
address,cite,code,em,th {font-weight:normal; font-style:normal;}
a{text-decoration: none;}

.clearfix{clear:both;*zoom:1;}


#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  width:1000px;
  margin: 0 auto;
  background: #fff;
  height: 100%;
}
</style>
