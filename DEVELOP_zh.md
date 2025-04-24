# 辩论模拟器开发指南

本文档提供项目结构概述，并解释不同组件如何协同工作以创建英式议会辩论模拟体验。

## 项目架构

辩论模拟器采用模块化架构，将不同功能分离：

```
Debate Stimulator/
├── main.py                 # 主应用程序入口点
├── config.json             # 配置设置
├── config_utils.py         # 访问配置的工具
├── debater.py              # 辩手代理实现
├── debater_speech_structure.py # 不同位置的演讲模板
├── speaker.py              # 主席/主持人实现
├── interaction.py          # 语音转文本和文本转语音功能
├── team_brainstorm.py      # 团队准备和论点生成
├── progress_tracker.py     # 跟踪和分析辩论表现
├── text_generator.py       # 大语言模型提供商接口
├── tests/                  # 单元和集成测试
└── debate_history/         # 存储的辩论历史（运行时创建）
```

## 核心组件

### 1. 主应用程序流程 (`main.py`)

主模块协调整个辩论过程：
- 使用议题初始化辩论
- 设置主席、辩手和头脑风暴
- 管理不同位置之间的演讲流程
- 处理人类参与者的音频录制
- 处理语音转文本和文本转语音转换
- 保存辩论历史并提供进度分析

### 2. 配置系统 (`config.json` & `config_utils.py`)

配置系统允许自定义：
- AI提供商设置（OpenAI、OpenRouter）
- 不同组件的模型选择
- 主席和辩手的语音语调
- 每个辩论位置的角色分配（人类vs AI）

### 3. 辩论参与者

#### 主席 (`speaker.py`)
主席作为辩论主持人：
- 宣布议题并开始辩论
- 依次介绍每位发言者
- 管理发言者之间的过渡
- 结束辩论会话

#### 辩手 (`debater.py`)
辩手代表辩论中的每个参与者：
- 实现英式议会辩论中的8个不同位置
- 使用来自`debater_speech_structure.py`的特定位置模板
- 基于议题、之前的演讲和团队准备发表演讲
- 可配置为AI或人类参与者

### 4. 团队准备 (`team_brainstorm.py`)

BrainStormer组件模拟团队准备：
- 为每个团队生成战略论点
- 从不同角度分析议题
- 预测对方论点并准备反驳
- 为辩手提供线索和谈话要点

### 5. 语音交互 (`interaction.py`)

交互模块处理语音通信：
- 为AI演讲实现文本转语音（TTS）
- 为人类演讲实现语音转文本（STT）
- 支持不同的提供商后端（目前为OpenAI）
- 应用适当的语调和说话风格

### 6. 进度跟踪 (`progress_tracker.py`)

ProgressTracker随时间分析辩论表现：
- 将辩论历史保存到JSON文件
- 跟踪多次辩论的参与情况
- 识别需要改进的领域
- 生成个性化建议
- 提供辩论技能发展的分析

## 数据流

1. **初始化**：
   - 应用程序以议题开始
   - 从`config.json`加载配置
   - 初始化主席、辩手和头脑风暴组件

2. **准备阶段**：
   - BrainStormer生成团队特定论点
   - 主席宣布议题并开始辩论

3. **辩论阶段**：
   - 按顺序对每个位置：
     - 如果是AI：辩手通过TTS生成并发表演讲
     - 如果是人类：系统录制音频，通过STT转换为文本
   - 主席管理发言者之间的过渡

4. **结束阶段**：
   - 主席结束辩论
   - 保存辩论历史
   - 分析进度并提供反馈

## AI集成

系统以多种方式使用语言模型：

1. **团队头脑风暴**：使用模型为每个团队生成战略论点
2. **演讲生成**：为AI辩手创建特定位置的演讲
3. **语音交互**：将文本转换为语音，将语音转换为文本
4. **进度分析**：分析辩论表现并提供反馈

## 添加新功能

### 添加新的AI提供商

要添加新的AI提供商：
1. 使用新提供商的方法更新`interaction.py`文件
2. 在`text_generator.py`中添加特定提供商的实现
3. 更新`config.json`中的配置选项

### 添加新的辩论格式

要支持其他辩论格式：
1. 在`debater_speech_structure.py`中创建新的演讲模板
2. 更新`speaker.py`中的发言顺序
3. 修改`main.py`中的辩论流程

### 增强进度跟踪

要改进进度跟踪：
1. 扩展`progress_tracker.py`中的分析方法
2. 添加新的指标或可视化功能
3. 实现更复杂的反馈机制

## 测试

`tests/`目录包含各种组件的单元和集成测试：
- `test_main_audio.py`：音频录制和处理测试
- `debater_test.py`：辩手组件测试
- `speaker_test.py`：主席组件测试
- `test_progress_tracker.py`：进度跟踪功能测试

使用pytest运行测试：
```
pytest tests/
```

## 配置参考

`config.json`中的关键配置选项：

```json
{
  "speaker_tone": "...",        // 主席的语调指令
  "debater_tone": "...",        // 辩手的语调指令
  "TEAM_AI_PROVIDER": "...",    // 团队头脑风暴的提供商
  "TEAM_AI_MODEL": "...",       // 团队头脑风暴的模型
  "INDIVIDUAL_AI_PROVIDER": "...", // 个人辩手的提供商
  "INDIVIDUAL_AI_MODEL": "...",  // 个人辩手的模型
  "INTERACTION_PROVIDER": "...", // TTS/STT的提供商
  "PARTY": {                    // 角色分配（AI或人类）
    "Prime Minister": "AI",
    "Leader of Opposition": "AI",
    ...
  }
}
```

## 环境变量

应用程序需要以下环境变量：
- `OPENAI_API_KEY`：用于OpenAI服务
- `OPENROUTER_API_KEY`：用于OpenRouter服务
- `INTERACTION_KEY`：用于语音转文本和文本转语音服务

## 未来发展方向

潜在的增强领域：
1. **多语言支持**：添加对不同语言辩论的支持
2. **实时反馈**：在演讲期间提供即时反馈
3. **高级分析**：实现对辩论技巧的更复杂分析
4. **Web界面**：创建基于Web的UI以便更轻松地交互
5. **额外的AI提供商**：支持更多LLM提供商和模型
6. **辩论录制**：保存辩论的音频录音以供回顾

*[English Version (英文版)](DEVELOP.md)*
