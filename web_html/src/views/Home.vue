<template>
    <div class="home">

        <!-- 导航目录 -->
        <div class="header-nav">
            <el-menu
                    :default-active="activeIndex2"
                    class="el-menu-demo"
                    mode="horizontal"
                    @select="handleSelect"
                    background-color="#545c64"
                    text-color="#fff"
                    active-text-color="#ffd04b"
            >
                <template v-for="(item, index) in bookTypeList">
                    <el-menu-item :index="String(index)" :key="index" @click="queryBookList(item.id)">
                        <!--            <router-link :to="'/book_list?type=' + item.id" >-->
                        {{item.name}}
                        <!--            </router-link>-->
                    </el-menu-item>
                </template>
            </el-menu>
        </div>

        <div style="margin-top: 15px;" class="search">
            <el-input placeholder="请输入内容" v-model="input3" class="input-with-select">
                <el-select v-model="select" slot="prepend" placeholder="请选择">

                    <el-option v-for="(item, index) in inputList" :key="index" :label="item.name"
                               :value="item.value"></el-option>

                </el-select>
                <el-button slot="append" class="mybutton" @click="search">搜索</el-button>
            </el-input>
        </div>

        <router-view ref="contentBox"/>


    </div>
</template>

<script>
    // @ is an alias to /src
    import axios from "axios"
    import store from "../store/index"

    export default {
        name: "Home",
        data() {
            return {
                activeIndex2: "0",
                bookTypeList: [{name: "首页"}],
                inputList: [
                    {name: "书名", value: 1},
                    {name: "作者", value: 2},
                ],
                input3: '',
                select: ""
            };
        },
        components: {},

        mounted() {
            this.getBookType();
        },
        methods: {

            getBookType() {
                this.activeIndex2 = this.$store.state.SideBarIndex

                axios.get("/webBook/web/book_type/",).then((data) => {

                    this.status = data.data.status
                    if (this.status == 1) {
                        // console.log(data.data.results)
                        data.data.results.forEach((item) => {
                            this.bookTypeList.push({name: item.type_name, id: item.id})
                        })
                    } else {
                        // console.log(1)
                    }
                })
            },
            queryBookList(val) {
                if (val) {
                    this.$router.push({path: "/book_list", query: {type: val}})
                } else {
                    this.$router.push({path: "/"})
                }
            },
            handleSelect(index) {
                this.$store.commit("changeSideBarIndex", index)

            },
            search() {
                console.log(this.select)

                this.loading = true;
                this.bookList = []
                axios.post("/webBook/web/search/", {

                    query_type: this.select,
                    content: this.input3,
                    page: this.currentPage,
                    page_size: this.pageSize

                }).then((data) => {

                    this.status = data.data.status
                    this.loading = false
                    this.total = data.data.counts

                    let results = data.data.results
                    for (let i in results) {
                        data = results[i]
                        // console.log(data)
                        this.bookList.push(data)
                    }

                    if(this.$route.name !== 'BookList'){
                        this.$router.push({name:"BookList"})
                    }

                    this.$nextTick(()=>{
                        // 分发查询 书籍列表数据
                        if(this.$refs.contentBox.refreshBookList){
                            this.$refs.contentBox.refreshBookList(this.bookList)
                        }

                        // todo 分发其他页面相关业务数据



                    })

                })

            },

        }


    };
</script>
<style scoped>
    .home {
        height: 100%;
    }

    .mybutton {
        color: #FFF !important;
        background-color: #409eff !important;
        border-color: #409eff !important;
    }

    .search {
        display: flex;
        justify-content: flex-end;
        margin-right: 20px;
    }

</style>
<style>
    .el-select .el-input {
        width: 90px;
    }

    .search .el-input-group {
        width: 400px;
    }

</style>
