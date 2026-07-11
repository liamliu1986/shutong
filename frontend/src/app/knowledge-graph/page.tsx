'use client';

import React, { useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';

interface KnowledgePoint {
  id: number;
  name: string;
  mastery: number;
}

const KnowledgeGraphPage: React.FC = () => {
  const [selectedSubject, setSelectedSubject] = useState('数学');

  // 模拟知识点数据
  const knowledgeData: Record<string, KnowledgePoint[]> = {
    '数学': [
      { id: 1, name: '函数与导数', mastery: 85 },
      { id: 2, name: '三角函数', mastery: 70 },
      { id: 3, name: '数列', mastery: 60 },
      { id: 4, name: '立体几何', mastery: 45 },
      { id: 5, name: '解析几何', mastery: 30 },
      { id: 6, name: '概率统计', mastery: 75 },
    ],
    '物理': [
      { id: 1, name: '力学', mastery: 80 },
      { id: 2, name: '电磁学', mastery: 55 },
      { id: 3, name: '光学', mastery: 70 },
      { id: 4, name: '热学', mastery: 65 },
    ],
    '化学': [
      { id: 1, name: '有机化学', mastery: 50 },
      { id: 2, name: '无机化学', mastery: 75 },
      { id: 3, name: '化学反应原理', mastery: 60 },
    ],
    '英语': [
      { id: 1, name: '语法', mastery: 80 },
      { id: 2, name: '阅读理解', mastery: 65 },
      { id: 3, name: '写作', mastery: 55 },
      { id: 4, name: '听力', mastery: 70 },
    ],
  };

  const subjects = Object.keys(knowledgeData);
  const currentPoints = knowledgeData[selectedSubject] || [];

  const getMasteryColor = (mastery: number) => {
    if (mastery >= 80) return 'bg-green-500';
    if (mastery >= 60) return 'bg-blue-500';
    if (mastery >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-800">知识图谱</h1>

        {/* 学科选择按钮 */}
        <div className="flex gap-4">
          {subjects.map((subject) => (
            <button
              key={subject}
              onClick={() => setSelectedSubject(subject)}
              className={`px-6 py-2 rounded-lg transition-colors ${
                selectedSubject === subject
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {subject}
            </button>
          ))}
        </div>

        {/* 知识点列表 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            {selectedSubject} - 知识点掌握度
          </h2>
          <div className="space-y-4">
            {currentPoints.map((point) => (
              <div key={point.id} className="border-b pb-4 last:border-0">
                <div className="flex justify-between mb-1">
                  <span className="text-gray-800 font-medium">{point.name}</span>
                  <span className="text-gray-500">{point.mastery}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`${getMasteryColor(point.mastery)} h-3 rounded-full transition-all duration-500`}
                    style={{ width: `${point.mastery}%` }}
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

export default KnowledgeGraphPage;