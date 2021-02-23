<template>
    <div id="readerlist">
        <ul v-loading="loading" :element-loading-text="text" element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.8)">

            <!-- 书籍名称 -->
            <li class="fj">
                <h3>{{this.$route.query.book_name}}</h3>
                <div class="border-line"></div>
            </li>

            <!-- 章节列表 -->
            <li v-for="(item, index) in bookChapterList" :key="index">
                <!--                before_id=bookChapterList[index-1]-->
                <a @click="read(item,index)">{{item.chapter_name}}</a>
            </li>


        </ul>

        <div class="block">
            <el-pagination
                    class="pagination"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[100, 150, 200]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>
        </div>
    </div>


</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                bookChapterList: [],
                currentPage: 1,
                pageSize: 100,
                total: 0,
                loading: false,
                text: "拼命加载中",
            };
        },
        computed: {},

        mounted() {
            this.book_chapter();

            // console.log(this.$route, '--------------------')
        },
        methods: {

            book_chapter() {
                this.loading = true;
                axios.get("/webBook/web/book_chapter/", {
                    params: {
                        book: this.$route.query.book,
                        page: this.currentPage,
                        page_size: this.pageSize
                    },
                }).then((data) => {
                    this.loading = false
                    this.status = data.data.status
                    this.bookChapterList = data.data.results
                    this.total = data.data.counts
                })
            },

            book_detail(id) {
                this.$router.push({path: "/book_detail", query: {book: id}})
            },

            read(item, index) {
                // let obj = {
                //     chapter: item,
                //     index: index,
                //     book_id: this.$route.query.book,
                // }
                // console.log(item, "_------------------------")
                // this.$store.commit("getChapter", obj)
                // this.$router.push({name: "BookRead"})
                // console.log(item.book_id)
                this.$router.push({path: "/book_read", query: {book_id: item.book_id.id, "chapter_num": item.num}})
            },


            handleSizeChange(val) {
                this.pageSize = val
                this.book_chapter()
            },
            handleCurrentChange(val) {
                this.currentPage = val
                this.book_chapter()

            }


        }
    };
</script>

<style scoped>

    #readerlist {
        float: left;
        border: 1px solid #d8d8d8;
        border-top: none;
        width: 988px;
        background: #FFF;
        padding-bottom: 55px;
        font-family: 微软雅黑, 宋体;
        position: relative;
        height: calc(100% - 61px);
    }

    #readerlist ul {
        margin: 0 20px;
        color: #949494;
        height: 100%;
    }

    #readerlist ul h3 {
        color: #208181;
        font-weight: bold;
        font-size: 15px;
        border: 1px solid #d8d8d8;
        background-color: #f7f7f7;
        margin-top: 5px;
        text-align: center;
    }

    #readerlist ul .fj {
        width: 945px;
        padding: 0px;
        margin: 0px;
    }

    #readerlist ul li {
        line-height: 30px;
        width: 224px;
        border-bottom: 1px solid #eee;
        float: left;
        overflow: hidden;
        padding-left: 10px;
        text-overflow: ellipsis;
        white-space: nowrap;
        cursor: pointer;
    }

    #readerlist ul li a {
        text-decoration: none;
        color: #333;
        font-size: 12px;
    }

    #readerlist ul li a:hover {
        color: #208181;
        text-decoration: none
    }

    #readerlist ul li a:visited {
        color: #949494
    }

    #readerlist .short_block {
        float: left;
        width: 941px;
        line-height: 25px;
        padding-left: 10px;
    }

    .readerts {
        border: 1px solid #ddd;
        background: #fff;
        margin: 0 auto;
        width: 978px;
        position: relative;
        height: 180px;
        padding-left: 10px;
        color: #949494;
        line-height: 20px;
    }

    .readerts h4 {
        color: #f60;
        padding-top: 10px
    }

    .border-line {
        margin-top: 1px;
        border-top: 1px solid #d8d8d8;
        padding-top: 3px;
    }

    .block {
        position: absolute;
        bottom: 20px;
        right: 20px;
    }

</style>