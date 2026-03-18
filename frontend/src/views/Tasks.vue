<template>
  <div class="tasks">
    <div class="container">
      <div class="header">
        <h1 class="page-title">我的任务</h1>
        <el-button type="primary" @click="goToCreate">
          <el-icon><Plus /></el-icon>
          创建新绘本
        </el-button>
      </div>

      <!-- 任务统计 -->
      <div class="stats">
        <div class="stat-card">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">全部任务</div>
        </div>
        <div class="stat-card">
          <div class="stat-value processing">{{ stats.processing }}</div>
          <div class="stat-label">处理中</div>
        </div>
        <div class="stat-card">
          <div class="stat-value completed">{{ stats.completed }}</div>
          <div class="stat-label">已完成</div>
        </div>
        <div class="stat-card">
          <div class="stat-value failed">{{ stats.failed }}</div>
          <div class="stat-label">失败</div>
        </div>
      </div>

      <!-- 任务列表 -->
      <div v-loading="loading" class="task-list">
        <el-empty v-if="!loading && tasks.length === 0" description="暂无任务">
          <el-button type="primary" @click="goToCreate">创建第一个绘本</el-button>
        </el-empty>

        <div v-else class="tasks-container">
          <div 
            v-for="task in tasks" 
            :key="task.id" 
            class="task-card"
            :class="{ 'failed': task.status === 'failed' }"
          >
            <div class="task-header">
              <div class="task-title">{{ task.title }}</div>
              <el-tag :type="getStatusType(task.status)" size="small">
                {{ getStatusText(task.status) }}
              </el-tag>
            </div>

            <div class="task-body">
              <div class="task-info">
                <div class="info-item">
                  <span class="label">创建时间:</span>
                  <span class="value">{{ formatDate(task.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">当前进度:</span>
                  <span class="value">{{ task.progress }}%</span>
                </div>
                <div class="info-item" v-if="task.retry_count > 0">
                  <span class="label">重试次数:</span>
                  <span class="value">{{ task.retry_count }}</span>
                </div>
              </div>

              <el-progress 
                :percentage="task.progress" 
                :status="getProgressStatus(task.status)"
                :show-text="true"
              />
            </div>

            <div class="task-footer">
              <div v-if="task.error_message" class="error-message">
                <el-icon><Warning /></el-icon>
                {{ task.error_message }}
              </div>

              <div class="task-actions">
                <el-button 
                  v-if="task.status === 'completed' && task.has_result"
                  type="primary" 
                  size="small"
                  @click="viewResult(task.id)"
                >
                  查看结果
                </el-button>
                
                <el-button 
                  v-if="task.status === 'failed'"
                  type="warning" 
                  size="small"
                  @click="handleRetry(task.id)"
                  :loading="retrying === task.id"
                >
                  重试
                </el-button>

                <el-button 
                  type="danger" 
                  size="small"
                  @click="handleDelete(task.id)"
                  :loading="deleting === task.id"
                >
                  删除
                </el-button>

                <el-button 
                  size="small"
                  @click="viewDetail(task.id)"
                >
                  详情
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详情对话框 -->
      <el-dialog
        v-model="detailDialogVisible"
        title="任务详情"
        width="70%"
      >
        <div v-if="currentTask" class="task-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="任务ID">{{ currentTask.id }}</el-descriptions-item>
            <el-descriptions-item label="任务标题">{{ currentTask.title }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(currentTask.status)">
                {{ getStatusText(currentTask.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="进度">{{ currentTask.progress }}%</el-descriptions-item>
            <el-descriptions-item label="当前步骤">{{ currentTask.current_step || '-' }}</el-descriptions-item>
            <el-descriptions-item label="重试次数">{{ currentTask.retry_count }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(currentTask.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ formatDate(currentTask.updated_at) }}</el-descriptions-item>
          </el-descriptions>

          <div v-if="currentTask.error_message" class="error-section">
            <h4>错误信息</h4>
            <el-alert type="error" :closable="false">
              {{ currentTask.error_message }}
            </el-alert>
          </div>

          <div v-if="taskProgress && taskProgress.length > 0" class="progress-section">
            <h4>执行进度</h4>
            <el-timeline>
              <el-timeline-item
                v-for="(p, index) in taskProgress"
                :key="index"
                :timestamp="formatDate(p.updated_at)"
                :type="getTimelineType(p.step_status)"
              >
                <strong>{{ getStepName(p.step_name) }}</strong>
                <p>{{ p.message }}</p>
                <p v-if="p.step_status === 'processing'">进度: {{ p.step_progress }}%</p>
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Warning } from '@element-plus/icons-vue'
import { getTasks, deleteTask as apiDeleteTask, retryTask, getTaskStatus } from '@/api'

const router = useRouter()
const loading = ref(false)
const tasks = ref([])
const currentTask = ref(null)
const taskProgress = ref([])
const detailDialogVisible = ref(false)
const retrying = ref(null)
const deleting = ref(null)

const stats = computed(() => {
  return {
    total: tasks.value.length,
    processing: tasks.value.filter(t => t.status === 'processing').length,
    completed: tasks.value.filter(t => t.status === 'completed').length,
    failed: tasks.value.filter(t => t.status === 'failed').length
  }
})

onMounted(() => {
  loadTasks()
})

async function loadTasks() {
  loading.value = true
  try {
    const response = await getTasks(50, 0)
    if (response.success) {
      tasks.value = response.tasks
    }
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

function getStatusType(status) {
  const typeMap = {
    pending: 'info',
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return typeMap[status] || 'info'
}

function getStatusText(status) {
  const textMap = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return textMap[status] || status
}

function getProgressStatus(status) {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return null
}

function getTimelineType(status) {
  const typeMap = {
    pending: 'info',
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return typeMap[status] || 'info'
}

function getStepName(step) {
  const stepMap = {
    task_created: '任务创建',
    uploading_images: '上传图片',
    story_generating: '生成故事',
    story_completed: '故事生成完成',
    images_generating: '生成插图',
    images_completed: '插图生成完成',
    finalizing: '最终处理'
  }
  return stepMap[step] || step
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

async function viewDetail(taskId) {
  try {
    const response = await getTaskStatus(taskId)
    if (response.success) {
      currentTask.value = response.task
      taskProgress.value = response.progress || []
      detailDialogVisible.value = true
    }
  } catch (error) {
    ElMessage.error('加载任务详情失败')
  }
}

async function handleRetry(taskId) {
  try {
    await ElMessageBox.confirm(
      '确定要重试这个任务吗？将从失败点继续执行。',
      '确认重试',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    retrying.value = taskId
    const response = await retryTask(taskId)
    
    if (response.success) {
      ElMessage.success('任务已重新开始处理')
      // 刷新任务列表
      setTimeout(loadTasks, 2000)
    } else {
      ElMessage.error(response.error || '重试失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('重试失败')
    }
  } finally {
    retrying.value = null
  }
}

async function handleDelete(taskId) {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个任务吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    deleting.value = taskId
    const response = await apiDeleteTask(taskId)
    
    if (response.success) {
      ElMessage.success('任务已删除')
      loadTasks()
    } else {
      ElMessage.error(response.error || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    deleting.value = null
  }
}

async function viewResult(taskId) {
  // 加载任务详情并保存结果
  try {
    const response = await getTaskStatus(taskId)
    if (response.success && response.task.result) {
      localStorage.setItem('generatedStorybook', JSON.stringify(response.task.result))
      router.push('/preview')
    }
  } catch (error) {
    ElMessage.error('加载结果失败')
  }
}

function goToCreate() {
  router.push('/create')
}
</script>

<style scoped>
.tasks {
  min-height: 100vh;
  padding: 40px 20px;
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
  margin-bottom: 40px;
}

.page-title {
  font-size: 36px;
  margin: 0;
}

/* 统计卡片 */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-value.processing {
  color: #e6a23c;
}

.stat-value.completed {
  color: #67c23a;
}

.stat-value.failed {
  color: #f56c6c;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

/* 任务列表 */
.task-list {
  min-height: 400px;
}

.tasks-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.task-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.task-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.task-card.failed {
  border: 2px solid #f56c6c;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.task-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.task-body {
  margin-bottom: 20px;
}

.task-info {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  font-size: 14px;
}

.label {
  color: #666;
}

.value {
  color: #333;
  font-weight: 500;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #f56c6c;
  font-size: 14px;
  margin-bottom: 15px;
  padding: 10px;
  background: #fef0f0;
  border-radius: 4px;
}

.task-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 详情 */
.task-detail {
  padding: 20px;
}

.error-section,
.progress-section {
  margin-top: 30px;
}

.error-section h4,
.progress-section h4 {
  margin-bottom: 15px;
  color: #333;
}

/* 响应式 */
@media (max-width: 768px) {
  .tasks-container {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 28px;
  }

  .header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
