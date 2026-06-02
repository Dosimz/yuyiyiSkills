# 视频转写流水线 - 使用指南

## 🎯 快速开始

### B站视频处理
```bash
# 1. 转写（自动下载+封面截取+转写）
cd ~/.hermes/skills/skills/video-to-text/scripts
/usr/bin/python3 transcribe.py "https://b23.tv/xxx" --duration 30 --no-organize

# 2. 排版（使用text-visualizer Agent）
# 主Agent会自动调度text-visualizer Agent

# 3. 发布（使用publisher脚本）
cd ~/skills/wechat_article_skills/wechat-draft-publisher
python3 -c "from publisher import WeChatPublisher; p = WeChatPublisher(); ..."
```

### 抖音视频处理
```bash
# 同样的流程，只是URL不同
cd ~/.hermes/skills/skills/video-to-text/scripts
/usr/bin/python3 transcribe.py "https://v.douyin.com/xxx" --duration 30 --no-organize
```

## 📁 目录结构
```
~/video-downloads/
├── bilibili/
│   ├── raw/         # 原始视频
│   ├── audio/       # 音频+转写结果
│   ├── covers/      # 封面图片
│   └── html/        # 排版HTML
├── douyin/
│   ├── raw/
│   ├── audio/
│   ├── covers/
│   └── html/
```

## 🖼️ 封面获取规则

**命名规则**：`<平台>_<标题>_cover.jpg`

**获取策略**（按优先级）：
1. 从视频平台获取封面图（yt-dlp --print thumbnail）
2. 从视频文件截取帧（ffmpeg -ss 1 -vframes 1）
3. 使用默认封面

**对应关系**：封面文件名和HTML文件名使用相同的标题，确保不会搞错

## 📝 排版主题

**wechat-ai-digest** 支持三种主题：
1. **digest**（默认）：蓝灰色系，适合大多数AI资讯
2. **magazine**：紫色系，适合深度分析
3. **notebook**：绿色系，适合技术教程

## ⚠️ 重要提醒

### 代理使用
- **代理端口10808**：专门用来访问GitHub
- **视频下载**：抖音/B站是大陆网站，**不需要挂代理**

### 微信安全
- 100%内联样式，禁止`<style>`标签
- 禁止class/id、flex/grid
- 容器max-width:677px

### 封面匹配
- publisher会根据文章标题自动匹配封面
- 精确匹配：`<平台>_<标题>_cover.jpg`
- 模糊匹配：`<平台>_<标题>*_cover.jpg`
- 回退到默认封面

## 🔧 故障排查

### 下载失败
- 检查网络连接
- 检查Cookie是否过期（抖音）
- 检查代理设置（GitHub用代理，视频下载不用）

### 转写失败
- 检查DASHSCOPE_API_KEY是否设置
- 检查音频文件是否完整
- 检查网络连接

### 排版失败
- 检查text-visualizer Agent是否可用
- 检查转写文本是否完整
- 检查wechat-ai-digest技能是否加载

### 发布失败
- 检查微信API配置
- 检查封面图片是否存在
- 检查HTML内容是否符合微信安全规范

## 📊 当前状态

**架构**：双Agent + 脚本
- 主Agent：执行transcribe.py和publisher.py
- text-visualizer Agent：生成HTML

**Token消耗**：约6,000-12,000 tokens/次

**已验证功能**：
- ✅ B站下载（支持b23.tv短链接）
- ✅ 抖音下载
- ✅ 封面截取
- ✅ 语音转写
- ✅ 排版（三主题）
- ✅ 发布到微信草稿箱

## 📚 相关文档

- **transcribe.py**: ~/.hermes/skills/skills/video-to-text/scripts/transcribe.py
- **publisher.py**: ~/skills/wechat_article_skills/wechat-draft-publisher/publisher.py
- **wechat-ai-digest**: ~/skills/wechat-ai-digest/SKILL.md
- **bilibili-to-wechat-pipeline**: ~/.hermes/skills/productivity/bilibili-to-wechat-pipeline/SKILL.md

---

**最后更新**：2026-06-01
**状态**：✅ 全流程验证通过
