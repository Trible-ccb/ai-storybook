<template>
  <div class="create">
    <div class="container">
      <h1 class="page-title">创作专属绘本</h1>
      
      <!-- 步骤指示器 -->
      <el-steps :active="currentStep" align-center class="steps">
        <el-step title="上传照片" />
        <el-step title="填写信息" />
        <el-step title="描述创意" />
        <el-step title="选择风格" />
        <el-step title="生成绘本" />
      </el-steps>

      <!-- 步骤1: 上传照片 -->
      <div v-show="currentStep === 0" class="step-content">
        <div class="upload-section">
          <div class="upload-item">
            <h3>1. 上传孩子照片</h3>
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :before-upload="handleChildPhotoUpload"
              action="#"
            >
              <img v-if="formData.child_photo" :src="formData.child_photo" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <p class="tip">请上传清晰的正面照片，光线充足</p>
          </div>

          <div class="upload-item">
            <h3>2. 上传玩具照片</h3>
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :before-upload="handleToyPhotoUpload"
              action="#"
            >
              <img v-if="formData.toy_photo" :src="formData.toy_photo" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <p class="tip">上传孩子最喜欢的玩具</p>
          </div>
        </div>
      </div>

      <!-- 步骤2: 填写信息 -->
      <div v-show="currentStep === 1" class="step-content">
        <el-form :model="formData" label-width="120px" class="info-form">
          <el-form-item label="孩子名字">
            <el-input v-model="formData.child_name" placeholder="例如：小美" />
          </el-form-item>
          
          <el-form-item label="孩子年龄">
            <el-select v-model="formData.age" placeholder="请选择">
              <el-option label="3岁" :value="3" />
              <el-option label="4岁" :value="4" />
              <el-option label="5岁" :value="5" />
              <el-option label="6岁" :value="6" />
              <el-option label="7岁" :value="7" />
              <el-option label="8岁" :value="8" />
              <el-option label="9岁" :value="9" />
              <el-option label="10岁" :value="10" />
              <el-option label="11岁" :value="11" />
              <el-option label="12岁" :value="12" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="玩具名字">
            <el-input v-model="formData.toys_name" placeholder="例如：小白兔" />
          </el-form-item>
          
          <el-form-item label="孩子特点">
            <el-input
              v-model="formData.child_characteristics"
              type="textarea"
              :rows="3"
              placeholder="例如：活泼可爱，喜欢穿粉色裙子"
            />
          </el-form-item>
          
          <el-form-item label="玩具特点">
            <el-input
              v-model="formData.toys_characteristics"
              type="textarea"
              :rows="2"
              placeholder="例如：毛绒玩具，有长长的耳朵"
            />
          </el-form-item>
        </el-form>
      </div>

      <!-- 步骤3: 描述创意 -->
      <div v-show="currentStep === 2" class="step-content">
        <div class="creative-form">
          <el-form label-width="120px">
            <el-form-item label="故事主题">
              <el-radio-group v-model="formData.theme">
                <el-radio label="友谊">友谊</el-radio>
                <el-radio label="勇气">勇气</el-radio>
                <el-radio label="学习">学习</el-radio>
                <el-radio label="环保">环保</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="异想天开">
              <el-input
                v-model="formData.creative_idea"
                type="textarea"
                :rows="6"
                placeholder="例如：小白兔会说话，带小美去森林里找彩虹糖..."
              />
            </el-form-item>
          </el-form>
          
          <div class="creative-tips">
            <h4>💡 创意灵感</h4>
            <ul>
              <li>玩具突然活过来了，带孩子去冒险</li>
              <li>孩子和玩具一起探索神秘的世界</li>
              <li>玩具教孩子学习新的知识和技能</li>
              <li>孩子和玩具一起解决困难</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 步骤4: 选择风格 -->
      <div v-show="currentStep === 3" class="step-content">
        <div class="style-selection">
          <h3>选择视觉风格</h3>
          <div class="style-options">
            <div 
              v-for="(style, index) in visualStyles" 
              :key="index"
              class="style-card"
              :class="{ 'selected': formData.visual_style === style.value }"
              @click="formData.visual_style = style.value"
            >
              <div class="style-preview" :style="{ background: style.color }">
                {{ style.icon }}
              </div>
              <h4>{{ style.name }}</h4>
              <p>{{ style.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 步骤5: 生成绘本 -->
      <div v-show="currentStep === 4" class="step-content">
        <div class="generating">
          <div v-if="generating">
            <el-icon class="is-loading" :size="80"><Loading /></el-icon>
            <h2>正在生成绘本...</h2>
            <p class="progress-text">{{ progressText }}</p>
            <el-progress :percentage="progress" :status="progress === 100 ? 'success' : ''" />
            <p class="tip-text">预计需要 5-10 分钟，请耐心等待...</p>
          </div>
          
          <div v-else class="generate-result">
            <el-result
              icon="success"
              title="绘本生成成功！"
              sub-title="您可以预览或直接下载"
            >
              <template #extra>
                <el-button type="primary" size="large" @click="goToPreview">
                  预览绘本
                </el-button>
                <el-button size="large" @click="resetForm">
                  再做一个
                </el-button>
              </template>
            </el-result>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <el-button v-if="currentStep > 0 && currentStep < 4" @click="prevStep">
          上一步
        </el-button>
        <el-button 
          v-if="currentStep < 4" 
          type="primary" 
          @click="nextStep"
          :disabled="!canProceed"
          :loading="currentStep === 3 && generating"
        >
          {{ currentStep === 3 ? '开始生成' : '下一步' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Loading } from '@element-plus/icons-vue'
import { generateCompleteStorybook, pollTaskStatus } from '@/api'

const router = useRouter()
const currentStep = ref(0)
const generating = ref(false)
const progress = ref(0)
const progressText = ref('')
const currentTaskId = ref(null)
const pollInterval = ref(null)

const formData = ref({
  child_photo: '',
  toy_photo: '',
  child_name: '',
  age: 5,
  toys_name: '',
  child_characteristics: '',
  toys_characteristics: '',
  theme: '友谊',
  creative_idea: '',
  visual_style: '水彩手绘',
  page_count: 12
})

const visualStyles = [
  {
    name: '水彩手绘',
    value: '水彩手绘',
    icon: '🎨',
    description: '柔和的水彩笔触，温暖色调，梦幻感',
    color: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
  },
  {
    name: '卡通风格',
    value: '卡通风格',
    icon: '🌈',
    description: '线条清晰，色彩鲜艳，造型可爱',
    color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  {
    name: '国风',
    value: '国风',
    icon: '🎋',
    description: '传统水墨风格，淡雅古典',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  }
]

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return formData.value.child_photo && formData.value.toy_photo
    case 1:
      return formData.value.child_name && formData.value.toys_name
    case 2:
      return formData.value.creative_idea
    case 3:
      return true
    default:
      return false
  }
})

function beforeUpload(file) {
  const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPGOrPNG) {
    ElMessage.error('只能上传JPG或PNG格式的图片')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  return true
}

// 将文件转为 base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = error => reject(error)
  })
}

// 处理孩子照片上传
async function handleChildPhotoUpload(file) {
  const isValid = beforeUpload(file)
  if (!isValid) return false

  try {
    const base64 = await fileToBase64(file)
    formData.value.child_photo = base64
    ElMessage.success('孩子照片上传成功')
  } catch (error) {
    ElMessage.error('照片处理失败')
  }

  return false // 阻止自动上传
}

// 处理玩具照片上传
async function handleToyPhotoUpload(file) {
  const isValid = beforeUpload(file)
  if (!isValid) return false

  try {
    const base64 = await fileToBase64(file)
    formData.value.toy_photo = base64
    ElMessage.success('玩具照片上传成功')
  } catch (error) {
    ElMessage.error('照片处理失败')
  }

  return false // 阻止自动上传
}

function nextStep() {
  if (currentStep.value === 3) {
    generateStorybook()
  } else {
    currentStep.value++
  }
}

function prevStep() {
  currentStep.value--
}

async function generateStorybook() {
  generating.value = true
  progress.value = 0
  progressText.value = '正在创建任务...'
  
  try {
    const request = {
      age: formData.value.age,
      theme: formData.value.theme,
      child_name: formData.value.child_name,
      child_characteristics: formData.value.child_characteristics,
      toys_name: formData.value.toys_name,
      toys_characteristics: formData.value.toys_characteristics,
      creative_idea: formData.value.creative_idea,
      visual_style: formData.value.visual_style,
      child_photo: formData.value.child_photo,
      page_count: formData.value.page_count
    }
    
    // 第一步：创建任务
    const createResponse = await generateCompleteStorybook(request)
    
    if (!createResponse.success) {
      throw new Error(createResponse.error || '创建任务失败')
    }
    
    currentTaskId.value = createResponse.task_id
    progress.value = 10
    progressText.value = '任务已创建，开始生成...'
    
    // 第二步：轮询任务状态
    const result = await pollTaskStatus(
      currentTaskId.value,
      (task) => {
        // 更新进度
        progress.value = task.progress || 10
        progressText.value = task.progress_text || '处理中...'
      },
      3000,  // 每3秒查询一次
      60     // 最多查询60次（3分钟）
    )
    
    // 任务完成
    progress.value = 100
    progressText.value = '生成完成！'
    
    // 保存生成的绘本数据
    localStorage.setItem('generatedStorybook', JSON.stringify(result))
    
    setTimeout(() => {
      generating.value = false
      ElMessage.success('绘本生成成功！')
    }, 500)
    
  } catch (error) {
    generating.value = false
    
    if (error.message.includes('超时')) {
      ElMessage.error('生成超时，请稍后在预览页面查看结果')
      // 可以保存任务ID，稍后继续查询
      if (currentTaskId.value) {
        localStorage.setItem('pendingTaskId', currentTaskId.value)
      }
    } else {
      ElMessage.error('生成失败：' + error.message)
    }
    
    // 恢复到上一步，允许用户重试
    currentStep.value = 3
  }
}

function goToPreview() {
  router.push('/preview')
}

function resetForm() {
  currentStep.value = 0
  formData.value = {
    child_photo: '',
    toy_photo: '',
    child_name: '',
    age: 5,
    toys_name: '',
    child_characteristics: '',
    toys_characteristics: '',
    theme: '友谊',
    creative_idea: '',
    visual_style: '水彩手绘',
    page_count: 12
  }
  localStorage.removeItem('generatedStorybook')
  currentTaskId.value = null
}
</script>

<style scoped>
.create {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f9f9f9;
}

.page-title {
  text-align: center;
  font-size: 36px;
  margin-bottom: 40px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.steps {
  margin-bottom: 60px;
}

.step-content {
  min-height: 400px;
}

/* 上传 */
.upload-section {
  display: flex;
  gap: 40px;
  justify-content: center;
  flex-wrap: wrap;
}

.upload-item {
  text-align: center;
}

.upload-item h3 {
  margin-bottom: 20px;
  font-size: 18px;
}

.avatar-uploader {
  width: 300px;
  height: 300px;
  border: 2px dashed #d9d9d9;
  border-radius: 10px;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader:hover {
  border-color: #667eea;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: 60px;
  color: #ccc;
}

.tip {
  margin-top: 15px;
  color: #999;
  font-size: 14px;
}

/* 表单 */
.info-form {
  max-width: 600px;
  margin: 0 auto;
}

/* 创意 */
.creative-form {
  max-width: 700px;
  margin: 0 auto;
}

.creative-tips {
  margin-top: 30px;
  padding: 20px;
  background: #f0f9ff;
  border-radius: 8px;
}

.creative-tips h4 {
  margin-bottom: 15px;
  color: #667eea;
}

.creative-tips ul {
  list-style: none;
  padding: 0;
}

.creative-tips li {
  padding: 8px 0;
  color: #666;
  padding-left: 20px;
  position: relative;
}

.creative-tips li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #667eea;
  font-size: 20px;
  line-height: 1;
}

/* 风格选择 */
.style-selection h3 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.style-options {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.style-card {
  width: 250px;
  padding: 30px;
  border: 2px solid #eee;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.style-card:hover {
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
}

.style-card.selected {
  border-color: #667eea;
  background: #f0f9ff;
}

.style-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
}

.style-card h4 {
  margin-bottom: 10px;
  font-size: 18px;
}

.style-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

/* 生成中 */
.generating {
  text-align: center;
  padding: 60px 20px;
}

.generating .is-loading {
  margin-bottom: 20px;
  color: #667eea;
}

.generating h2 {
  margin-bottom: 20px;
  color: #333;
}

.progress-text {
  margin-bottom: 30px;
  color: #666;
  font-size: 16px;
}

.tip-text {
  margin-top: 20px;
  color: #999;
  font-size: 14px;
}

.generate-result {
  padding: 40px 20px;
}

/* 操作按钮 */
.actions {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .upload-section {
    flex-direction: column;
  }
  
  .style-options {
    flex-direction: column;
  }
  
  .page-title {
    font-size: 28px;
  }
}
</style>
