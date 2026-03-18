<template>
  <div class="payment">
    <div class="container">
      <h1 class="page-title">确认订单</h1>
      
      <div class="order-content">
        <!-- 订单信息 -->
        <div class="order-info">
          <h2>订单信息</h2>
          <div class="info-item">
            <span class="label">绘本标题：</span>
            <span class="value">{{ storybook?.title || '我的专属绘本' }}</span>
          </div>
          <div class="info-item">
            <span class="label">页数：</span>
            <span class="value">{{ storybook?.pages?.length || 0 }}页</span>
          </div>
          <div class="info-item">
            <span class="label">主角：</span>
            <span class="value">{{ formData.child_name }}</span>
          </div>
          <div class="info-item">
            <span class="label">视觉风格：</span>
            <span class="value">{{ formData.visual_style }}</span>
          </div>
        </div>

        <!-- 套餐选择 -->
        <div class="plan-selection">
          <h2>选择套餐</h2>
          <div class="plan-cards">
            <div 
              v-for="(plan, index) in plans" 
              :key="index"
              class="plan-card"
              :class="{ 'selected': selectedPlan === index }"
              @click="selectedPlan = index"
            >
              <div v-if="plan.popular" class="popular-badge">热门</div>
              <h3>{{ plan.name }}</h3>
              <div class="price">
                <span class="price-value">¥{{ plan.price }}</span>
                <span class="price-unit">/本</span>
              </div>
              <ul class="features-list">
                <li v-for="(feature, fIndex) in plan.features" :key="fIndex">
                  ✓ {{ feature }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 支付方式 -->
        <div class="payment-method">
          <h2>支付方式</h2>
          <div class="payment-options">
            <div 
              class="payment-option"
              :class="{ 'selected': paymentMethod === 'wechat' }"
              @click="paymentMethod = 'wechat'"
            >
              <div class="option-icon">💚</div>
              <div class="option-info">
                <h4>微信支付</h4>
                <p>推荐使用</p>
              </div>
            </div>
            
            <div 
              class="payment-option"
              :class="{ 'selected': paymentMethod === 'alipay' }"
              @click="paymentMethod = 'alipay'"
            >
              <div class="option-icon">💙</div>
              <div class="option-info">
                <h4>支付宝</h4>
                <p>快捷支付</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 价格明细 -->
        <div class="price-summary">
          <div class="summary-item">
            <span class="label">原价：</span>
            <span class="value">¥{{ originalPrice }}</span>
          </div>
          <div class="summary-item discount">
            <span class="label">优惠：</span>
            <span class="value">-¥{{ discount }}</span>
          </div>
          <div class="summary-item total">
            <span class="label">实付：</span>
            <span class="value">¥{{ finalPrice }}</span>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="submit-section">
          <el-button 
            type="primary" 
            size="large" 
            @click="submitOrder"
            :loading="submitting"
          >
            确认支付 ¥{{ finalPrice }}
          </el-button>
          <el-button size="large" @click="goBack">
            返回
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const submitting = ref(false)
const selectedPlan = ref(1)
const paymentMethod = ref('wechat')
const storybook = ref(null)
const formData = ref({})

const plans = [
  {
    name: '基础版',
    price: 99,
    features: [
      '12页数字绘本',
      'PDF格式',
      '单一风格',
      '5分钟生成'
    ],
    popular: false
  },
  {
    name: '标准版',
    price: 199,
    features: [
      '16页数字绘本',
      'PDF + 有声',
      '3种风格可选',
      '优先生成'
    ],
    popular: true
  },
  {
    name: '尊享版',
    price: 399,
    features: [
      '20页数字绘本',
      'PDF + 有声 + AR',
      '精装实体书',
      '专属客服'
    ],
    popular: false
  }
]

const originalPrice = computed(() => {
  return plans[selectedPlan.value].price
})

const discount = computed(() => {
  // 首单优惠30元
  return 30
})

const finalPrice = computed(() => {
  return Math.max(0, originalPrice.value - discount.value)
})

onMounted(() => {
  const savedStorybook = localStorage.getItem('generatedStorybook')
  const savedFormData = localStorage.getItem('formData')
  
  if (savedStorybook) {
    storybook.value = JSON.parse(savedStorybook)
  }
  
  if (savedFormData) {
    formData.value = JSON.parse(savedFormData)
  }
})

function goBack() {
  router.back()
}

function submitOrder() {
  submitting.value = true
  
  // 模拟提交订单
  setTimeout(() => {
    submitting.value = false
    ElMessage.success('订单提交成功！即将跳转到支付页面...')
    
    // 这里应该调用支付接口
    // window.location.href = paymentUrl
    
    // 演示：直接跳转到成功页面
    setTimeout(() => {
      router.push('/preview')
    }, 1500)
  }, 2000)
}
</script>

<style scoped>
.payment {
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
}

.order-content {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

/* 订单信息 */
.order-info {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #eee;
}

.info-item {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  width: 100px;
  color: #999;
}

.value {
  color: #333;
  font-weight: 500;
}

/* 套餐选择 */
.plan-selection {
  margin-bottom: 40px;
}

.plan-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.plan-card {
  flex: 1;
  min-width: 280px;
  padding: 30px;
  border: 2px solid #eee;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.plan-card:hover {
  border-color: #667eea;
}

.plan-card.selected {
  border-color: #667eea;
  background: #f0f9ff;
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #667eea;
  color: white;
  padding: 5px 20px;
  border-radius: 20px;
  font-size: 14px;
}

.plan-card h3 {
  font-size: 20px;
  margin-bottom: 15px;
}

.price {
  margin-bottom: 20px;
}

.price-value {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
}

.price-unit {
  font-size: 16px;
  color: #999;
}

.features-list {
  list-style: none;
  padding: 0;
  text-align: left;
}

.features-list li {
  padding: 8px 0;
  color: #666;
}

/* 支付方式 */
.payment-method {
  margin-bottom: 40px;
}

.payment-options {
  display: flex;
  gap: 20px;
}

.payment-option {
  flex: 1;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s;
}

.payment-option:hover {
  border-color: #667eea;
}

.payment-option.selected {
  border-color: #667eea;
  background: #f0f9ff;
}

.option-icon {
  font-size: 32px;
}

.option-info h4 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.option-info p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

/* 价格明细 */
.price-summary {
  margin-bottom: 40px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item.discount .value {
  color: #f56c6c;
}

.summary-item.total {
  font-size: 20px;
  font-weight: bold;
  margin-top: 10px;
  padding-top: 15px;
  border-top: 2px solid #ddd;
}

.summary-item.total .value {
  color: #667eea;
  font-size: 28px;
}

/* 提交按钮 */
.submit-section {
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .plan-cards {
    flex-direction: column;
  }
  
  .payment-options {
    flex-direction: column;
  }
  
  .submit-section {
    flex-direction: column;
  }
  
  .submit-section button {
    width: 100%;
  }
}
</style>
