'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';

interface Mistake {
  id: number;
  subject: string;
  chapter: string;
  content: string;
  difficulty: '简单' | '中等' | '困难';
  date: string;
}

const MistakesPage: React.FC = () => {
  const [filterSubject, setFilterSubject] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');

  // 模拟错题数据
  const mistakes: Mistake[] = [
    {
      id: 1,
      subject: '数学',
      chapter: '函数与导数',
      content: '求函数f(x)=x³-3x的极值',
      difficulty: '中等',
      date: '2026-07-09',
    },
    {
      id: 2,
      subject: '物理',
      chapter: '电磁感应',
      content: '计算感应电动势的大小',
      difficulty: '困难',
      date: '2026-07-08',
    },
    {
      id: 3,
      subject: '英语',
      chapter: '虚拟语气',
      content: 'If I were you, I would...',
      difficulty: '简单',
      date: '2026-07-07',
    },
  ];

  const filteredMistakes = mistakes.filter((mistake) => {
    const subjectMatch = filterSubject === 'all' || mistake.subject === filterSubject;
    const difficultyMatch = filterDifficulty === 'all' || mistake.difficulty === filterDifficulty;
    return subjectMatch && difficultyMatch;
  });

  const difficultyColor = {
    '简单': 'bg-green-100 text-green-800',
    '中等': 'bg-yellow-100 text-yellow-800',
    '困难': 'bg-red-100 text-red-800',
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">错题本</h1>
          <Link
            href="/mistakes/add"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            添加错题
          </Link>
        </div>

        {/* 筛选功能 */}
        <div className="bg-white rounded-lg shadow p-4 flex gap-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">科目</label>
            <select
              value={filterSubject}
              onChange={(e) => setFilterSubject(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="all">全部科目</option>
              <option value="数学">数学</option>
              <option value="物理">物理</option>
              <option value="化学">化学</option>
              <option value="英语">英语</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">难度</label>
            <select
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="all">全部难度</option>
              <option value="简单">简单</option>
              <option value="中等">中等</option>
              <option value="困难">困难</option>
            </select>
          </div>
        </div>

        {/* 错题列表 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMistakes.map((mistake) => (
            <div key={mistake.id} className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm text-gray-500">{mistake.subject}</span>
                <span className={`text-xs px-2 py-1 rounded ${difficultyColor[mistake.difficulty]}`}>
                  {mistake.difficulty}
                </span>
              </div>
              <p className="text-gray-800 mb-2">{mistake.content}</p>
              <div className="flex justify-between items-center text-sm text-gray-400">
                <span>{mistake.chapter}</span>
                <span>{mistake.date}</span>
              </div>
            </div>
          ))}
        </div>

        {filteredMistakes.length === 0 && (
          <div className="text-center py-12 text-gray-500">暂无错题记录</div>
        )}
      </div>
    </MainLayout>
  );
};

export default MistakesPage;