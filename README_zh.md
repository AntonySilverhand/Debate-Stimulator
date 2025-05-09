# 辩论模拟器 - 英式议会辩论练习

一款先进的AI驱动工具，用于练习英式议会辩论，获取反馈并随时间跟踪您的进步。

*[English Version (英文版)](README.md)*

## 概述

辩论模拟器提供了一个真实的环境，让您可以与AI对手或队友练习英式议会（BP）辩论。系统允许您：

- 参与完整的8位发言者BP格式辩论
- 与具有高级修辞能力的AI辩手进行练习
- 使用语音转文本技术记录和转录您的演讲
- 通过文本转语音功能聆听AI演讲
- 跟踪您的进步并获取个性化改进建议
- 保存辩论历史以供日后回顾和分析

## 英式议会辩论格式

英式议会（BP）辩论格式涉及4个队伍的8位发言者：

1. **开幕政府方**
   - 首相
   - 副首相

2. **开幕反对方**
   - 反对党领袖
   - 副反对党领袖

3. **闭幕政府方**
   - 政府成员
   - 政府党鞭

4. **闭幕反对方**
   - 反对党成员
   - 反对党党鞭

每位发言者按顺序发表演讲，各自有特定的角色和责任。

## 功能特点

- **AI辩手**：由最先进的语言模型驱动，提供具有挑战性的对手
- **语音交互**：记录您的演讲并听取AI回应，获得自然的辩论体验
- **可定制议题**：使用各种辩论主题进行练习
- **团队头脑风暴**：AI辅助演讲准备
- **进度跟踪**：随时间分析您的进步情况
- **辩论历史**：保存并回顾过去的辩论，创造学习机会

## 开始使用

1. 克隆此仓库
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 在`config.json`中配置您的偏好：
   - 设置哪些位置由人类或AI扮演
   - 调整演讲语调和AI模型
4. 运行应用程序：
   ```
   python main.py
   ```

## 配置

编辑`config.json`以自定义：
- 哪些辩论位置由人类或AI填充
- AI提供商和模型选择
- 发言者和辩手语调设置
- 其他辩论参数

## 使用方法

1. 以预定议题开始辩论会话
2. 提示时，按Enter键开始录音，发表您的演讲
3. 再次按Enter键结束录音
4. 聆听AI回应，并在适用情况下准备您的下一次演讲
5. 在辩论结束时查看进度分析

## 进度跟踪

系统会随时间跟踪您的辩论表现，提供：
- 整体技能发展指标
- 特定改进领域
- 未来练习建议

## 系统要求

- Python 3.8+
- 麦克风和扬声器
- 互联网连接（用于AI服务）
- 所需Python包（见requirements.txt）

## 许可证

本项目采用GNU Affero通用公共许可证v3.0（AGPL-3.0）：

- **开源**：必须向所有用户提供完整的源代码
- **网络保护**：如果您在服务器上运行修改版本，必须公开源代码
- **Copyleft**：衍生作品必须在相同的许可证下分发
- **署名**：应给予原作者（AntonySilverhand）适当的署名

完整详情请参阅[LICENSE](LICENSE)英文版或[LICENSE_zh.md](LICENSE_zh.md)中文版，也可查看[AGPL-3.0许可证](https://www.gnu.org/licenses/agpl-3.0.html)官方网站。

## 贡献者

AntonySilverhand

---

*通过AI驱动的反馈进行刻意练习，提高您的辩论技巧。*
