<template>
  <div class="preview">
    <div class="container">
      <div class="header">
        <h1 class="page-title">绘本预览</h1>
        <div class="actions">
          <el-button @click="goBack">返回</el-button>
          <el-button type="primary" @click="downloadPDF">下载PDF</el-button>
          <el-button type="success" @click="goToPayment">支付并获取</el-button>
        </div>
      </div>

      <div v-if="storybook" class="storybook-preview">
        <div v-for="(page, index) in storybook.pages" :key="index" class="page">
          <img :src="page.image_url" :alt="`第${page.page}页`" class="page-image" />
          <p class="page-text">{{ page.text }}</p>
        </div>
      </div>
      
      <div v-else class="empty">
        <el-empty description="暂无绘本数据" />
        <el-button type="primary" @click="goToCreate">去创作</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import html2pdf from 'html2pdf.js'

const router = useRouter()
const storybook = ref(null)

onMounted(() => {
  const savedStorybook = localStorage.getItem('generatedStorybook')
  if (savedStorybook) {
    storybook.value = JSON.parse(savedStorybook)
  }
})

function goBack() {
  router.back()
}

function goToCreate() {
  router.push('/create')
}

function goToPayment() {
  router.push('/payment')
}

function downloadPDF() {
  if (!storybook.value) {
    ElMessage.warning('没有可下载的绘本')
    return
  }
  
  ElMessage.info('正在生成PDF...')
  
  // 创建HTML内容
  const content = document.createElement('div')
  
  storybook.value.pages.forEach((page, index) => {
    const pageElement = document.createElement('div')
    pageElement.style.cssText = `
      page-break-after: always;
      padding: 40px;
      text-align: center;
      font-family: 'Arial', sans-serif;
    `
    
    pageElement.innerHTML = `
      <img src="${page.image_url}" style="max-width: 100%; height: 400px; object-fit: contain; margin-bottom: 20px;" />
      <p style="font-size: 18px; line-height: 1.6; color: #333;">${page.text}</p>
    `
    
    content.appendChild(pageElement)
  })
  
  // 生成PDF
  const opt = {
    margin: 10,
    filename: `${storybook.value.title || '绘本'}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }
  
  html2pdf().set(opt).from(content).save()
    .then(() => {
      ElMessage.success('PDF下载成功')
    })
    .catch((error) => {
      ElMessage.error('PDF生成失败：' + error.message)
    })
}
</script>

<style scoped>
.preview {
  min-height: 100vh;
  padding: 20px;
  background: #f9f9f9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 10px;
}

.page-title {
  font-size: 28px;
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.storybook-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.page {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.page-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 15px;
}

.page-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  text-align: center;
}

.empty {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 10px;
}

/* 响应式 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
  }
  
  .actions {
    width: 100%;
    justify-content: center;
  }
  
  .storybook-preview {
    grid-template-columns: 1fr;
  }
}
</style>
