# 智能旅行助手

从[datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)中单独提出并修改的模块。
感谢作者提供最初的工程原型！致敬。

## 🏗️ 技术栈

### 后端

- **框架**: LangGraph & LangChain
- **API**: FastAPI
- **MCP工具**: amap-mcp-server (高德地图)
- **LLM**: 支持多种LLM提供商(OpenAI, DeepSeek等)

### 前端

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design Vue
- **地图服务**: 高德地图 JavaScript API
- **HTTP客户端**: Axios

### 数据库

- postgre

## ✨ 功能特点

- 🤖 **AI驱动的旅行规划**: 使用LangGraph & LangChain智能生成详细的多日旅程、大概经济预算
- 🧩 **postgre数据库持久化存储**:用户标记、QA部分、携带物品、预约抢票标记服务等
- 🗺️ **高德地图集成**: 通过MCP协议接入高德地图服务,支持景点搜索、路线规划、天气查询
- 🧠 **智能工具调用**: Agent自动调用高德地图MCP工具,获取实时POI、路线和天气信息
- 🎨 **现代化前端**: Vue3 + TypeScript + Vite,响应式设计,流畅的用户体验
- 📱 **完整功能**: 包含住宿、交通、餐饮和景点游览时间推荐


## znn：开发版本更新标记

v 0.3.1 ：postgreSQL
- 初步设计表结构，并加入测试数据
- 测试与postgreSQL的连接，并将读取到的数据显示在前端

v 0.2.1 ：高德地图API接入
- 在amap canvas中显示Agent生成的地点，并粗略标明顺序、天数。（待仔细调整）
- 增加地图中的地点搜索、展示功能。
- 加入地点位置精确标识：倒置水滴。
- 准备接入postgre数据库...学习postgre操作

v 0.1.1 ：旅行生成内容修缮
- 对旅程内容单独提出作为一个页面。(trvlEdit.vue)

v 0.1.0 ：LangGraph替代原生Agent框架成功！
- 各接口功能测试均已通过。
- 不再依赖原生HelloAgents！
- 修缮前端的文件结构，使其有序。

v 0.0.2 ：后端修改
- 尝试Agent框架替换，学习接入

v 0.0.1 ：前端示例页面作placeholder
- Home和主页成分修改
- 新增票务预约页面。
- 新增物品显示页面

v 0.0.0 ：地基
- 学习LangChain、LangGraph、vue(vite、ant)、MCP、cursor & Zcode 使用、FastAPI

## Todo List
- 地图canvas每次切换禁用刷新


## 📁 项目结构
（不包括测试留存的垃圾文件！）

```
helloagents-trip-planner/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── agents/            # Agent实现
│   │   │   └── trip_planner_agent.py
│   │   ├── api/               # FastAPI路由
│   │   │   ├── main.py
│   │   │   └── routes/
│   │   │       ├── trip.py
│   │   │       └── map.py
│   │   │       └── poi.py  
│   │   ├── pgdb/              # postgre数据库对接层 
│   │   │   ├── connection .py 
│   │   ├── services/          # 服务层
│   │   │   ├── amap_service.py
│   │   │   └── llm_service.py
│   │   │   └── unsplash_service.py
│   │   ├── models/            # 数据模型
│   │   │   └── schemas.py
│   │   └── config.py          # 配置管理
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/                  # 前端应用
│   ├── public/
│   │   ├── avatar/            # 测试用头像组件 
│   │   ├── BGimage/           # 测试用图片 
│   ├── src/
│   │   ├── components/        # Vue组件
│   │   ├── services/          # API服务
│   │   ├── stores/            # 高德POI持久化服务
│   │   ├── types/             # TypeScript类型 与 临时测试数据
│   │   └── views/             # 页面视图
│   ├── package.json
│   └── vite.config.ts
└── Playground/                # 制作过程中的部分知识巩固标记
└── README.md
```


## 🙏 致谢

- [HelloAgents](https://github.com/datawhalechina/Hello-Agents) - 智能体教程
- [HelloAgents框架](https://github.com/jjyaoao/HelloAgents) - 智能体框架
- [高德地图开放平台](https://lbs.amap.com/) - 地图服务
- [amap-mcp-server](https://github.com/sugarforever/amap-mcp-server) - 高德地图MCP服务器

---
