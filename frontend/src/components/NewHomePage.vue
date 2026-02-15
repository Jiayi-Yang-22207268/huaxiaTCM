<template>
    <div id="wrapper">
      <!-- Header Section -->
      <header id="header" class="alt" v-animate-on-scroll="'fade-in'">
        <router-link to="/" class="logo"><strong>中药百科</strong> <span>中医学习平台</span></router-link>
        <nav><a href="#menu">Menu</a></nav>
      </header>
      <!-- Menu Navigation -->
      <nav id="menu">
        <ul class="links">
          <li><router-link to="/">主页</router-link></li>
          <li><router-link to="/quiz">Quiz</router-link></li>
          <li><router-link to="/game">小游戏</router-link></li>
          <li><router-link to="/encyclopedia">药方百科</router-link></li>
        </ul>
        <ul class="actions stacked">
          <li><router-link to="/register" class="button primary fit">注册</router-link></li>
          <li><router-link to="/login" class="button fit">登录</router-link></li>
        </ul>
      </nav>
      <!-- Banner Section -->
      <section id="banner" class="major">
        <div class="inner">
          <header class="major">
            <h1 v-animate-on-scroll="'slide-in-left'">欢迎来到中药学习网站</h1>
          </header>
          <div class="content" v-animate-on-scroll="'slide-in-left'">
            <p>这里有中医药的百科、测验和趣味互动</p>
            <ul class="actions">
              <li><a href="#one" class="button next scrolly">开始探索</a></li>
            </ul>
          </div>
        </div>
      </section>
      <!-- Main Content Area -->
      <div id="main">
        <section id="one" class="tiles">
          <article v-for="item in herbs" :key="item.id">
            <span class="image">
              <img :src="item.image" :alt="item.name" />
            </span>
            <header class="major">
              <h3><router-link :to="`/herb/${item.id}`" class="link">{{ item.name }}</router-link></h3>
              <p>{{ item.description }}</p>
            </header>
          </article>
        </section>
      </div>
    </div>

</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {

});
const herbs = [
  {
    id: 1,
    name: '当归',
    image: '/images/herbs/danggui.jpg',
    description: '补血调经，活血止痛'
  },
  {
    id: 2,
    name: '黄芪',
    image: '/images/herbs/huangqi.jpg',
    description: '益气固表，利尿托毒'
  }
  // Additional herb items can be added here
]
</script>

<style scoped>


.before-enter {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease;
}

.fade-in {
  opacity: 1;
  transform: translateY(0);
}

.slide-in-left {
  opacity: 1;
  transform: translateX(0);
}

.before-enter.slide-in-left {
  transform: translateX(-40px);
}
</style>