<template>
  <div class="home">
    <header class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          将孩子的异想天开<br>
          <span class="highlight">变成专属绘本</span>
        </h1>
        <p class="hero-subtitle">
          用 AI 技术为孩子创作独一无二的绘本故事<br>
          让想象力飞出童话世界
        </p>
        <div class="hero-buttons">
          <router-link to="/create" class="btn btn-primary">
            开始创作
          </router-link>
          <router-link to="/tasks" class="btn btn-secondary">
            我的任务
          </router-link>
        </div>
      </div>
      
      <div class="hero-visual">
        <div class="book-preview">
          <div class="book-page">📚</div>
          <div class="book-page">🎨</div>
          <div class="book-page">✨</div>
        </div>
      </div>
    </header>

    <!-- 特色功能 -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">为什么选择我们</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>角色真实</h3>
            <p>上传孩子照片，主角就是孩子自己</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI 智能创作</h3>
            <p>先进大模型生成适合孩子年龄的故事</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3>精美插图</h3>
            <p>多种风格可选，插图与角色一致</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <h3>快速生成</h3>
            <p>5-10 分钟完成整个绘本制作</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💾</div>
            <h3>任务管理</h3>
            <p>支持断点续传，失败后可重试</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>随时查看</h3>
            <p>任务列表中随时查看所有创作</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 创作流程 -->
    <section class="process">
      <div class="container">
        <h2 class="section-title">创作流程</h2>
        <div class="process-steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>上传照片</h3>
            <p>上传孩子和玩具的照片</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>填写信息</h3>
            <p>孩子名字、年龄和特点</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>描述创意</h3>
            <p>让孩子讲述他的异想天开</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>选择风格</h3>
            <p>水彩、卡通、国风等风格</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">5</div>
            <h3>生成绘本</h3>
            <p>AI 自动生成故事和插图</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 案例展示 -->
    <section id="examples" class="examples">
      <div class="container">
        <h2 class="section-title">优秀案例</h2>
        <div class="example-grid">
          <div class="example-card">
            <div class="example-image">🐰</div>
            <h3>小白兔的冒险</h3>
            <p>小美和她的玩具小白兔去森林找彩虹糖的故事</p>
            <div class="example-tags">
              <span class="tag">4岁</span>
              <span class="tag">水彩风格</span>
            </div>
          </div>
          <div class="example-card">
            <div class="example-image">🤖</div>
            <h3>机器人朋友</h3>
            <p>小明和他的玩具机器人一起学习科学知识</p>
            <div class="example-tags">
              <span class="tag">7岁</span>
              <span class="tag">卡通风格</span>
            </div>
          </div>
          <div class="example-card">
            <div class="example-image">🦄</div>
            <h3>独角兽的魔法</h3>
            <p>小丽和她的独角兽玩具一起探索魔法世界</p>
            <div class="example-tags">
              <span class="tag">6岁</span>
              <span class="tag">国风</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 价格方案 -->
    <section class="pricing">
      <div class="container">
        <h2 class="section-title">价格方案</h2>
        <div class="pricing-cards">
          <div class="pricing-card">
            <h3>基础版</h3>
            <div class="price">¥99<span>/本</span></div>
            <ul class="features">
              <li>12页数字绘本</li>
              <li>PDF格式</li>
              <li>单一风格</li>
              <li>5分钟生成</li>
            </ul>
            <button class="btn btn-outline" @click="goToCreate">开始创作</button>
          </div>
          <div class="pricing-card featured">
            <div class="badge">热门</div>
            <h3>标准版</h3>
            <div class="price">¥199<span>/本</span></div>
            <ul class="features">
              <li>16页数字绘本</li>
              <li>PDF + 有声</li>
              <li>3种风格可选</li>
              <li>优先生成</li>
            </ul>
            <button class="btn btn-primary" @click="goToCreate">开始创作</button>
          </div>
          <div class="pricing-card">
            <h3>尊享版</h3>
            <div class="price">¥399<span>/本</span></div>
            <ul class="features">
              <li>20页数字绘本</li>
              <li>PDF + 有声 + AR</li>
              <li>精装实体书</li>
              <li>专属客服</li>
            </ul>
            <button class="btn btn-outline" @click="goToCreate">开始创作</button>
          </div>
        </div>
        
        <div class="promotion">
          <p>🎉 <strong>首单优惠</strong>：下单立减 30 元！</p>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="faq">
      <div class="container">
        <h2 class="section-title">常见问题</h2>
        <div class="faq-list">
          <div class="faq-item">
            <h3>Q: 生成一本绘本需要多长时间？</h3>
            <p>A: 通常需要 5-10 分钟，取决于选择的套餐和服务器负载。</p>
          </div>
          <div class="faq-item">
            <h3>Q: 如果生成失败了怎么办？</h3>
            <p>A: 我们支持断点续传，失败后可以在"我的任务"中重试，从失败点继续生成。</p>
          </div>
          <div class="faq-item">
            <h3>Q: 支持哪些年龄段？</h3>
            <p>A: 目前支持 3-12 岁儿童，我们会根据年龄自动调整内容难度。</p>
          </div>
          <div class="faq-item">
            <h3>Q: 如何保证故事内容的适龄性？</h3>
            <p>A: 我们的 AI 经过专门训练，会根据孩子年龄调整词汇量和主题复杂度。</p>
          </div>
          <div class="faq-item">
            <h3>Q: 生成过程中可以关闭页面吗？</h3>
            <p>A: 可以！任务在后台运行，您可以在"我的任务"页面随时查看进度。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 AI 个性化绘本平台. All rights reserved.</p>
        <div class="version-info">
          <span>前端版本: {{ frontendVersion }}</span>
          <span>|</span>
          <span>后端版本: {{ backendVersion }}</span>
          <span>|</span>
          <span>构建时间: {{ buildTime }}</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 版本信息
const frontendVersion = ref('2.0.0')
const backendVersion = ref('加载中...')
const buildTime = ref('2024-03-18')

onMounted(async () => {
  // 获取后端版本信息
  try {
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
    const response = await axios.get(`${API_BASE_URL}/`)
    if (response.data && response.data.version) {
      backendVersion.value = response.data.version
    }
  } catch (error) {
    console.warn('获取后端版本失败:', error)
    backendVersion.value = '未知'
  }
})

function goToCreate() {
  router.push('/create')
}

function scrollToExamples() {
  document.getElementById('examples').scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  background: #f9f9f9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-content {
  max-width: 600px;
  z-index: 1;
}

.hero-title {
  font-size: 56px;
  line-height: 1.3;
  margin-bottom: 20px;
  font-weight: 800;
}

.hero-title .highlight {
  color: #fbbf24;
}

.hero-subtitle {
  font-size: 20px;
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn {
  padding: 15px 35px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #fbbf24;
  color: #333;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(251, 191, 36, 0.3);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  width: 100%;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.book-preview {
  display: flex;
  gap: 20px;
  perspective: 1000px;
}

.book-page {
  width: 150px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
  animation: float 3s ease-in-out infinite;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.book-page:nth-child(1) {
  animation-delay: 0s;
}

.book-page:nth-child(2) {
  animation-delay: 0.2s;
}

.book-page:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Features Section */
.features {
  padding: 100px 0;
  background: white;
}

.section-title {
  text-align: center;
  font-size: 42px;
  margin-bottom: 60px;
  color: #333;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-card {
  padding: 40px 30px;
  text-align: center;
  background: #f9f9f9;
  border-radius: 15px;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 50px;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

/* Process Section */
.process {
  padding: 100px 0;
  background: #f9f9f9;
}

.process-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.step {
  flex: 1;
  min-width: 180px;
  text-align: center;
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0 auto 20px;
}

.step h3 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.step p {
  color: #666;
  font-size: 14px;
}

.step-arrow {
  font-size: 40px;
  color: #667eea;
}

/* Examples Section */
.examples {
  padding: 100px 0;
  background: white;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.example-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.example-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.example-image {
  height: 200px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
}

.example-card h3 {
  padding: 20px;
  font-size: 22px;
  color: #333;
  margin-bottom: 10px;
}

.example-card > p {
  padding: 0 20px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.example-tags {
  padding: 0 20px 20px;
  display: flex;
  gap: 10px;
}

.tag {
  padding: 5px 15px;
  background: #f0f9ff;
  color: #667eea;
  border-radius: 20px;
  font-size: 14px;
}

/* Pricing Section */
.pricing {
  padding: 100px 0;
  background: #f9f9f9;
}

.pricing-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.pricing-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  position: relative;
  transition: all 0.3s;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.pricing-card.featured {
  border: 3px solid #667eea;
  transform: scale(1.05);
}

.pricing-card.featured:hover {
  transform: scale(1.05) translateY(-10px);
}

.badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: #667eea;
  color: white;
  padding: 8px 25px;
  border-radius: 20px;
  font-weight: bold;
}

.pricing-card h3 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.price {
  font-size: 48px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 30px;
}

.price span {
  font-size: 18px;
  color: #999;
  font-weight: normal;
}

.pricing-card ul {
  list-style: none;
  padding: 0;
  margin-bottom: 30px;
  text-align: left;
}

.pricing-card li {
  padding: 12px 0;
  color: #666;
  border-bottom: 1px solid #f0f0f0;
}

.pricing-card li::before {
  content: '✓ ';
  color: #667eea;
  font-weight: bold;
  margin-right: 10px;
}

.promotion {
  text-align: center;
  padding: 20px;
  background: #fff9e6;
  border-radius: 10px;
  font-size: 18px;
  color: #666;
}

.promotion strong {
  color: #667eea;
}

/* FAQ Section */
.faq {
  padding: 100px 0;
  background: white;
}

.faq-list {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: #f9f9f9;
  padding: 30px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.faq-item h3 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
}

.faq-item p {
  color: #666;
  line-height: 1.6;
}

/* Footer */
.footer {
  padding: 40px 0;
  background: #333;
  color: white;
  text-align: center;
}

.footer p {
  margin-bottom: 10px;
}

.footer .version-info {
  font-size: 12px;
  color: #999;
  margin-top: 10px;
}

.footer .version-info span {
  margin: 0 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    margin-bottom: 40px;
  }
  
  .hero-title {
    font-size: 42px;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .process-steps {
    flex-direction: column;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
  
  .pricing-card.featured {
    transform: scale(1);
  }
  
  .pricing-card.featured:hover {
    transform: translateY(-10px);
  }
}
</style>
