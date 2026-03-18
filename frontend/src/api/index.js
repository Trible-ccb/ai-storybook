import axios from 'axios'

// 从环境变量获取后端API地址
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// 创建axios实例
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000 // 30秒超时
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API错误:', error)

    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      return Promise.reject({
        isTimeout: true,
        message: '请求超时，但任务可能正在后台处理中'
      })
    }

    return Promise.reject(error)
  }
)

/**
 * 生成故事
 */
export async function generateStory(data) {
  return api.post('/generate-story', data)
}

/**
 * 一键生成完整绘本（持久化任务）
 */
export async function generateCompleteStorybook(data) {
  return api.post('/generate-complete-storybook', data)
}

/**
 * 查询任务状态
 */
export async function getTaskStatus(taskId) {
  return api.get(`/task/${taskId}`)
}

/**
 * 获取任务列表
 */
export async function getTasks(limit = 20, offset = 0, status = null) {
  const params = { limit, offset }
  if (status) {
    params.status = status
  }
  return api.get('/tasks', { params })
}

/**
 * 重试任务
 */
export async function retryTask(taskId) {
  return api.post(`/task/${taskId}/retry`)
}

/**
 * 删除任务
 */
export async function deleteTask(taskId) {
  return api.delete(`/task/${taskId}`)
}

/**
 * 轮询任务状态，直到完成或失败
 */
export async function pollTaskStatus(taskId, onProgress, interval = 3000, maxAttempts = 200) {
  let attempts = 0

  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        attempts += 1

        const response = await getTaskStatus(taskId)

        if (!response.success) {
          reject(new Error(response.error))
          return
        }

        const task = response.task

        // 调用进度回调
        if (onProgress) {
          onProgress(task, response.progress || [])
        }

        // 检查任务状态
        if (task.status === 'completed') {
          resolve(task.result)
          return
        }

        if (task.status === 'failed') {
          reject(new Error(task.error_message || '任务失败'))
          return
        }

        // 检查是否超过最大尝试次数
        if (attempts >= maxAttempts) {
          reject(new Error('任务超时，请稍后再试'))
          return
        }

        // 继续轮询
        setTimeout(poll, interval)

      } catch (error) {
        // 如果是网络错误，继续尝试轮询
        if (error.isNetworkError || error.code === 'ECONNRESET') {
          console.warn('网络错误，继续轮询...')
          setTimeout(poll, interval)
        } else {
          reject(error)
        }
      }
    }

    poll()
  })
}

export default api
