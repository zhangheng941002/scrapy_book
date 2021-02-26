module.exports = {
  lintOnSave: false,
  devServer:{
    disableHostCheck: true,
    proxy:{
      // "/api":{
      //   target:"http://172.31.0.9:14800",
      //   changeOrigin: true,  //是否跨域
      //   pathRewrite:{
      //     '/api':'/api'
      //   }
      // },
      "/webBook":{
        target:"http://192.168.200.42:8090/",
        changeOrigin: true,  //是否跨域
        pathRewrite:{
          '/webBook':''
        }
      }
    }
  }

}
