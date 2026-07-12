'use client';

import React, { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { mistakesAPI } from '@/lib/api';
import { Mistake } from '@/types';

const DIFFICULTY_LABELS: Record<number, string> = {
  1: '简单',
  2: '简单',
  3: '中等',
  4: '困难',
  5: '困难',
};

const DIFFICULTY_COLORS: Record<string, string> = {
  简单: 'bg-green-100 text-green-800',
  中等: 'bg-yellow-100 text-yellow-800',
  困难: 'bg-red-100 text-red-800',
};

const MistakesPage: React.FC = () => {
  const { user, isLoading: isAuthLoading } = useAuth();
  const [selectedChildId, setSelectedChildId] = useState<string>('');
  const [mistakes, setMistakes] = useState<Mistake[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const [filterSubject, setFilterSubject] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');

  // 默认选中第一个孩子
  useEffect(() => {
    if (user && user.children.length > 0 && !selectedChildId) {
      setSelectedChildId(user.children[0].id);
    }
  }, [user, selectedChildId]);

  // 拉取错题列表
  const fetchMistakes = useCallback((childId: string) => {
    setIsLoading(true);
    setError('');

    mistakesAPI
      .getMistakes({ child_id: childId })
      .then((response) => {
        setMistakes(response.data.items || []);
      })
      .catch((err) => {
        const detail = err.response?.data?.detail;
        setError(typeof detail === 'string' ? detail : '加载错题失败，请稍后重试');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!selectedChildId) return;
    fetchMistakes(selectedChildId);
  }, [selectedChildId, fetchMistakes]);

  const filteredMistakes = mistakes.filter((mistake) => {
    const difficultyLabel = DIFFICULTY_LABELS[mistake.difficulty] || '中等';
    const subjectMatch = filterSubject === 'all' || mistake.subject === filterSubject;
    const difficultyMatch = filterDifficulty === 'all' || difficultyLabel === filterDifficulty;
    return subjectMatch && difficultyMatch;
  });

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('zh-CN');
  };

  if (isAuthLoading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <span className="text-gray-500">加载中...</span>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return (
      <MainLayout>
        <div className="text-center py-12 text-gray-500">请先登录</div>
      </MainLayout>
    );
  }

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

        <div className="bg-white rounded-lg shadow p-4 flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-600 mb-1">孩子</label>
            <select
              value={selectedChildId}
              onChange={(e) => setSelectedChildId(e.target.value)}
              className="border rounded px-3 py-2"
            >
              <option value="">请选择孩子</option>
              {user.children.map((child) => (
                <option key={child.id} value={child.id}>
                  {child.name}
                </option>
              ))}
            </select>
          </div>
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

        {isLoading && (
          <div className="flex justify-center items-center h-64">
            <span className="text-gray-500">加载中...</span>
          </div>
        )}

        {error && !isLoading && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm flex justify-between items-center">
            <span>{error}</span>
            <button
              type="button"
              onClick={() => fetchMistakes(selectedChildId)}
              className="px-3 py-1 border border-red-300 rounded hover:bg-red-100 transition-colors"
            >
              重试
            </button>
          </div>
        )}

        {!isLoading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredMistakes.map((mistake) => {
                const difficultyLabel = DIFFICULTY_LABELS[mistake.difficulty] || '中等';
                return (
                  <div
                    key={mistake.id}
                    className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-500">{mistake.subject}</span>
                        {mistake.grade && (
                          <span className="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                            {mistake.grade}
                          </span>
                        )}
                      </div>
                      <span
                        className={`text-xs px-2 py-1 rounded ${DIFFICULTY_COLORS[difficultyLabel]}`}
                      >
                        {difficultyLabel}
                      </span>
                    </div>
                    <p className="text-gray-800 mb-2 line-clamp-3">{mistake.question_text}</p>
                    <div className="flex justify-between items-center text-sm text-gray-400">
                      <span>{mistake.chapter}</span>
                      <span>{formatDate(mistake.created_at)}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {filteredMistakes.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                {mistakes.length === 0 ? '暂无错题记录' : '暂无匹配结果'}
              </div>
            )}
          </>
        )}
      </div>
    </MainLayout>
  );
};

export default MistakesPage;
