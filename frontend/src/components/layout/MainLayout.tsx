'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface MainLayoutProps {
  children: React.ReactNode;
  username?: string;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, username = '用户' }) => {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navItems = [
    { href: '/dashboard', label: '首页', icon: '📊' },
    { href: '/children', label: '孩子管理', icon: '👶' },
    { href: '/knowledge-graph', label: '知识图谱', icon: '📚' },
    { href: '/mistakes', label: '错题本', icon: '📝' },
    { href: '/question-bank', label: '题库管理', icon: '❓' },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* 左侧导航菜单 */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-20'
        } bg-white shadow-md transition-all duration-300 flex flex-col`}
      >
        <div className="p-4 border-b">
          <h1 className={`font-bold text-xl text-blue-600 ${sidebarOpen ? 'block' : 'hidden'}`}>
            书童
          </h1>
          {!sidebarOpen && <span className="text-2xl">📖</span>}
        </div>
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center p-3 rounded-lg transition-colors ${
                    pathname === item.href
                      ? 'bg-blue-100 text-blue-700'
                      : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <span className="text-xl mr-3">{item.icon}</span>
                  {sidebarOpen && <span>{item.label}</span>}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-4 border-t text-gray-500 hover:text-gray-700"
        >
          {sidebarOpen ? '◀' : '▶'}
        </button>
      </aside>

      {/* 主内容区域 */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* 顶部导航栏 */}
        <header className="bg-white shadow-sm">
          <div className="flex items-center justify-between p-4">
            <h2 className="text-lg font-semibold text-gray-800">智能学习助手</h2>
            <div className="flex items-center space-x-4">
              <span className="text-gray-600">{username}</span>
              <button className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors">
                退出
              </button>
            </div>
          </div>
        </header>

        {/* 页面内容 */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
};

export default MainLayout;