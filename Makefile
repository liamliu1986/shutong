.PHONY: help build up down test logs clean shell backend frontend

help:
	@echo "书童 - 智能学习助手 (All-in-One Docker)"
	@echo ""
	@echo "可用命令:"
	@echo "  make build     - 构建所有镜像"
	@echo "  make up        - 启动所有服务"
	@echo "  make down      - 停止所有服务"
	@echo "  make test      - 运行后端测试"
	@echo "  make logs      - 查看服务日志"
	@echo "  make clean     - 清理容器、卷和镜像"
	@echo "  make shell     - 进入后端容器"
	@echo "  make backend   - 只启动后端和数据库"
	@echo "  make frontend  - 进入前端开发容器"

build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

test:
	docker-compose -f docker-compose.yml run --rm backend-test

logs:
	docker-compose -f docker-compose.yml logs -f

clean:
	docker-compose -f docker-compose.yml down -v --rmi local

shell:
	docker-compose -f docker-compose.yml exec backend bash

backend:
	docker-compose -f docker-compose.yml up -d mongodb neo4j backend

frontend:
	docker-compose -f docker-compose.yml up -d frontend
