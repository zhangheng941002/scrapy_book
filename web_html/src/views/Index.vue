<template>
    <div id="sitebox" v-loading="loading" :element-loading-text="text" element-loading-spinner="el-icon-loading"
         element-loading-background="rgba(0, 0, 0, 0.8)">

        <!-- 书籍列表 -->
        <dl v-for="(item, index) in bookList" :key="index">
            <dt>
                <!--        <a href="http://www.iqiwx.com/book/13375.html">-->
                <!--        <a :href="'/book_detail?book='+item.id">-->
                <img
                        :src="item.img"
                        :alt="item.book_name"
                        height="155"
                        width="120"
                        @click="book_detail(item.id, item.book_name)"
                        style="cursor: pointer"

                />
            </dt>
            <dd>
                <h3>
                    <!--          <span class="uptime">{{item.update_date}}</span>-->
                    <a @click="book_detail(item.id, item.book_name)">{{item.book_name}}</a>
                </h3>
            </dd>
            <dd class="book_other">
                作者：<span
            ><a
                    href="/modules/article/authorarticle.php?author=邪心未泯"
                    target="_blank"
                    rel="nofollow"
            >{{item.author_id.author_name}}</a
            ></span
            >状态：<span>连载中</span>
            </dd>
            <dd class="book_des">
                {{item.book_intro}}
            </dd>
            <dd class="book_yuedu">
                <a @click="book_detail(item.id, item.book_name)" target="_blank">章节目录</a>
                <a href="#" onclick="addbookcase(13375,0);">加入书架</a>
                <a href="javascript:void(0)" onclick="vote(13375,0);">推荐此书</a>
            </dd>
            <dd class="book_other">
                最新章节：<a href="/book/13/13375/37529476.html">第五零四八章 扩张</a>
            </dd>
        </dl>

        <div class="clearfix"></div>


        <div class="block">
            <el-pagination
                    class="pagination"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[20, 50, 100]"
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
                bookList: [],
                currentPage: 1,
                pageSize: 20,
                total: 0,
                loading: false,
                text: "拼命加载中"
            };
        },
        computed: {
            getBookType() {
                return this.$route.query.book_list
            }
        },
        watch: {
            getBookType: function () {
                this.bookList = this.$route.query.book_list
            },
        },
        mounted() {
            // this.searchBook();
            // console.log(this.$route)
            // if(this.$route.params && this.$route.params.book_list){
            //     this.bookList = this.$route.params.book_list
            // }

        },
        methods: {

            // searchBook() {
            //     this.loading = true;
            //     this.bookList = []
            //     axios.post("/webBook/web/search/", {
            //
            //         query_type: this.$route.query.query_type,
            //         content: this.$route.query.content,
            //         page: this.currentPage,
            //         page_size: this.pageSize
            //
            //     }).then((data) => {
            //
            //         this.status = data.data.status
            //         this.loading = false
            //         this.total = data.data.counts
            //
            //         let results = data.data.results
            //         for (let i in results) {
            //             data = results[i]
            //             // console.log(data)
            //             this.bookList.push(data)
            //         }
            //     })
            // },
            refreshBookList(bookList){
                this.bookList = bookList
            },
            book_detail(id, name) {
                this.$router.push({path: "/book_detail", query: {book: id, book_name: name}})
            },

            handleSizeChange(val) {
                this.pageSize = val
                this.getBookTypeInfo()
            },
            handleCurrentChange(val) {
                this.currentPage = val
                this.getBookTypeInfo()

            }


        }
    };
</script>

<style scoped>

</style>