<template>
    <div id="center">
        <!-- 标题 -->
        <div class="title" id="title">
            <h1>{{chapter_name}}</h1>
            作者:<span
        ><a
                href="/modules/article/authorarticle.php?author=邪心未泯"
                rel="nofollow"
        > {{author_name}}</a
        >
      </span>
            本章节字数:
            <span>12285K</span>
            更新时间:
            <span>{{create_date}}</span>
        </div>

        <!-- 内容 -->
        <div id="content" style="font-size: 24px" v-html="content">

        </div>

        <!--下一章  -->
        <div class="jump">
            <a @click="before_chapter">&lt;&lt;上一章</a>
            <!--      <a href="#" onclick="vote(13375);">投推荐票</a> -->
            <a @click="roll_back_chapter_list()">回目录</a>
            <!--      <a href="#" onclick="addbookcase(13375,35630);">标记书签</a>-->
            <a @click="next_chapter">下一章&gt;&gt;</a>
        </div>


    </div>
</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                chapter_name: "",
                content: "",
                book_id: 0,
                book_name: "",
                chapter_num: 0,
                author_name:"",
                create_date: ""
            };
        },
        computed: {

        },

        mounted() {
            this.book_id = this.$route.query.book_id

            this.chapter_content()
        },
        methods: {


            chapter_content(chapter_num) {
                if (!chapter_num){
                    chapter_num = this.$route.query.chapter_num
                }
                document.getElementById("title").scrollIntoView();
                axios.get("/webBook/web/chapter_content/", {
                    params: {
                        book: this.$route.query.book_id,
                        chapter_num: chapter_num
                    },
                }).then((data) => {

                    let res = data.data.results[0]
                    this.author_name = res.book_id.author_id.author_name
                    this.chapter_name = res.chapter_name
                    this.content = res.chapter_content
                    this.chapter_num = res.num
                    this.create_date = res.create_date
                    this.book_name = res.book_id.book_name
                    console.log("-------------", this.book_name)


                })
            },


            roll_back_chapter_list() {
                this.$router.push({path:"/book_detail", query:{
                    book:this.book_id,
                    book_name: this.book_name
                }})
            },
            before_chapter() {
                document.getElementById("title").scrollIntoView();
                this.chapter_num --
                this.chapter_content(this.chapter_num)
            },

            next_chapter() {
                document.getElementById("title").scrollIntoView();
                this.chapter_num ++
                this.chapter_content(this.chapter_num)
            },




        }
    };
</script>

<style>
    #center {
        overflow: hidden;
        border-top: 1px dotted #c0c6cb;
        margin-bottom: 5px;
        background-color: rgb(231, 244, 254);
    }

    .title {
        text-align: center;
        margin-top: 20px;
        position: relative;
        width: 100%;
        color: #999;
        padding-bottom: 10px;
        font-family: 微软雅黑, 宋体;
        font-size: 14px;
    }

    .title_l {
        text-align: center;
        margin-top: 5px;
        position: relative;
        width: 100%;
        color: #999;
        padding-bottom: 10px;
        font-family: 微软雅黑, 宋体;
        font-size: 14px;
    }

    .title h1 {
        font-size: 29px;
        color: #d40909;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .title span,
    .title_l span {
        color: #333;
        margin: 0 5px;
    }

    .adsgg {
        font-size: 20px;
        color: #555;
    }

    #content {
        line-height: 28px;
        padding-top: 10px;
        word-wrap: break-word;
        letter-spacing: 0.2em;
        line-height: 150%;
        width: 95%;
        color: #555;
        margin: auto;
        text-align: left;
        font-family: "方正启体简体", "微软雅黑", "宋体", "Microsoft YaHei", Arial,
        serif;
        font-size: 22px;
    }

    #content p {
        line-height: 150%;
        margin-bottom: 20px;
        text-align: left;
    }

    #content img {
        margin: 0 auto;
    }

    #content .watermark {
        display: none;
    }

    .jump {
        text-align: center;
        border-top: 1px dotted #c0c6cb;
        padding: 15px 0;
        width: 95%;
        margin: auto;
        cursor: pointer;
    }

    .jump1 {
        text-align: center;
        border-top: 1px #c0c6cb;
        padding: 2px 0;
        width: 95%;
        margin: auto;
    }

    .jump span {
        color: #b5b5b5;
        margin: 0 5px;
    }

    .jump a {
        line-height: 35px;
        color: #666;
        font-size: 14px;
        text-decoration: none;
        background: #ccc no-repeat -150px -43px;
        width: 111px;
        height: 35px;
        display: inline-block;
        margin: 0 5px;
    }

    .jump a.disabled {
        background: #f5f5f5 none;
        opacity: 0.8;
        color: #999;
        background: #ccc no-repeat -150px -43px;
        width: 111px;
        height: 35px;
        line-height: 35px;
        display: inline-block;
    }
</style>