'use client';

import React from 'react';
import MainLayout from '@/components/layout/MainLayout';

interface Question {
  id: number;
  subject: string;
  type: string;
  content: string;
  difficulty: '简单' | '中等' | '困难';
}

const QuestionBankPage: React.FC = () => {
  // 模拟题目数据
  const questions: Question[] = [
    {
      id: 1,
      subject: '数学',
      type: '选择题',
      content: '已知集合A={1,2,3}，B={2,3,4}，则A∩B=',
      difficulty: '简单',
    },
    {
      id: 2,
      subject: '物理',
      type: '计算题',
      content: '一个物体从静止开始做匀加速直线运动...',
      difficulty: '中等',
    },
    {
      id: 3,
      subject: '化学',
      type: '填空题',
      content: '写出下列反应的化学方程式...',
      difficulty: '简单',
    },
    {
      id: 4,
      subject: '英语',
      type: '阅读理解',
      content: 'Read the following passage and answer...',
      difficulty: '困难',
    },
  ];

  // 统计信息
  const stats = {
    total: questions.length,
    bySubject: {
      数学: questions.filter((q) => q.subject === '数学').length,
      物理: questions.filter((q) => q.subject === '物理').length,
      化学: questions.filter((q) => q.subject === '化学').length,
      英语: questions.filter((q) => q.subject === '英语').length,
    },
  };

  const difficultyColor = {
    '简单': 'bg-green-100 text-green-800',
    '中等': 'bg-yellow-100 text-yellow-800',
    '困难': 'bg-red-100 text-red-800',
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-800">题库管理</h1>

        {/* 统计信息 */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="bg-white rounded-lg shadow p-4 text-center">
            <p className="text-sm text-gray-500">总题数</p>
            <p className="text-2xl font-bold text-blue-600">{stats.total}</p>
          </div>
          {Object.entries(stats.bySubject).map(([subject, count]) => (
            <div key={subject} className="bg-white rounded-lg shadow p-4 text-center">
              <p className="text-sm text-gray-500">{subject}</p>
              <p className="text-2xl font-bold text-gray-800">{count}</p>
            </div>
          ))}
        </div>

        {/* 题目列表 */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">科目</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">题型</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">题目</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">难度</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {questions.map((question) => (
                <tr key={question.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-500">{question.subject}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{question.type}</td>
                  <td className="px-6 py-4 text-sm text-gray-800">{question.content}</td>
                  <td className="px-6 py-4">
                    <span className={`text-xs px-2 py-1 rounded ${difficultyColor[question.difficulty]}`}>
                      {question.difficulty}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </MainLayout>
  );
};

export default QuestionBankPage;