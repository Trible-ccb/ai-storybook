import axios from 'axios'

// 从环境变量获取后端API地址
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// 创建axios实例
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 60000
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
 * 一键生成完整绘本
 */
export async function generateCompleteStorybook(data) {
  return api.post('/generate-complete-storybook', data)
}

export default api
