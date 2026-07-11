'use client';

import React from 'react';
import MainLayout from '@/components/layout/MainLayout';

const DashboardPage: React.FC = () => {
  // 模拟数据
  const stats = {
    todayTasks: 5,
    totalMistakes: 42,
    weeklyGoal: 70,
  };

  const progressData = [
    { subject: '数学', progress: 65 },
    { subject: '物理', progress: 45 },
    { subject: '化学', progress: 80 },
    { subject: '英语', progress: 55 },
  ];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* 欢迎信息 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold text-gray-800">欢迎回来，同学！</h1>
          <p className="text-gray-600 mt-2">今天也要继续加油哦！</p>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm">今日任务</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">{stats.todayTasks}</p>
            <p className="text-gray-400 text-sm mt-1">待完成</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm">错题总数</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">{stats.totalMistakes}</p>
            <p className="text-gray-400 text-sm mt-1">需复习</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm">本周目标</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">{stats.weeklyGoal}%</p>
            <p className="text-gray-400 text-sm mt-1">完成度</p>
          </div>
        </div>

        {/* 学习进度概览 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">学习进度概览</h2>
          <div className="space-y-4">
            {progressData.map((item) => (
              <div key={item.subject}>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-700">{item.subject}</span>
                  <span className="text-gray-500">{item.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div
                    className="bg-blue-600 h-4 rounded-full transition-all duration-500"
                    style={{ width: `${item.progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;