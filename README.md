# resume-polish-lite

零依赖的**简历经历润色器**：把「负责……」「做了……」这类大白话，自动改写成「动作动词开头 + 量化结果」的专业简历 bullet。可选接入 LLM 做更自然的润色；没有 key 时本地规则已能完成改写。

## 功能简介

- 自动把弱动词（负责 / 参与 / 协助 / 做了）替换为强动作动词（主导 / 搭建 / 实现……）。
- 抽取经历中的量化数字（百分比、毫秒、金额、数量等），保留关键结果。
- 缺少量化结果时给出补全提示，提醒你补上数据。
- 可选 LLM 进一步润色。

## 快速开始

```bash
python3 cli.py --line "负责用户后台系统，做了权限模块，性能提升了30%"

# 从文件批量处理（每行一条）
python3 cli.py --file experience.txt
```

## 无 API key 如何运行

本项目**默认纯规则运行**，无需任何 key，立即输出改写后的 bullet。
仅当你想要更自然的措辞时，才需要：

```bash
export OPENAI_API_KEY=sk-xxx
python3 cli.py --line "负责用户后台系统" --llm
```

## 目录说明

```
resume-polish-lite/
├── resume_polish.py   # 弱动词替换 + 数字抽取 + 模板 + 可选 LLM
├── cli.py           # 命令行入口
├── tests/
│   └── test_resume.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
