'use client';

import React, { useCallback, useEffect, useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { knowledgeGraphAPI } from '@/lib/api';
import type { Subject, SubjectGraph } from '@/types';
import GraphCanvas from '@/components/graph/GraphCanvas';
import axios from 'axios';

/**
 * 知识图谱页面
 *
 * 展示学科知识点的交互式关系图
 * 支持学科切换、孩子选择、掌握度颜色显示
 */
const KnowledgeGraphPage: React.FC = () => {
  const { user, isLoading: isAuthLoading } = useAuth();

  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('');
  const [graph, setGraph] = useState<SubjectGraph | null>(null);
  const [isLoadingSubjects, setIsLoadingSubjects] = useState(false);
  const [isLoadingGraph, setIsLoadingGraph] = useState(false);
  const [error, setError] = useState('');
  const [isInitLoading, setIsInitLoading] = useState(false);
  const [selectedChildId, setSelectedChildId] = useState('');
  const [masteryMap, setMasteryMap] = useState<Record<string, number>>({});

  // 默认选中第一个孩子
  useEffect(() => {
    if (user && user.children.length > 0 && !selectedChildId) {
      setSelectedChildId(user.children[0].id);
    }
  }, [user, selectedChildId]);

  // 加载学科列表
  const fetchSubjects = useCallback(() => {
    setIsLoadingSubjects(true);
    setError('');

    knowledgeGraphAPI
      .getSubjects()
      .then((response) => {
        const data = response.data;
        setSubjects(data);
        if (data.length > 0 && !selectedSubjectId) {
          setSelectedSubjectId(data[0].id);
        }
      })
      .catch((err: unknown) => {
        let message = '加载学科列表失败，请稍后重试';
        if (axios.isAxiosError(err)) {
          const detail = err.response?.data?.detail;
          if (typeof detail === 'string') message = detail;
        }
        setError(message);
      })
      .finally(() => {
        setIsLoadingSubjects(false);
      });
  }, [selectedSubjectId]);

  useEffect(() => {
    if (user) {
      fetchSubjects();
    }
  }, [user, fetchSubjects]);

  // 加载学科图谱
  const fetchGraph = useCallback((subjectId: string) => {
    if (!subjectId) return;

    setIsLoadingGraph(true);
    setError('');

    knowledgeGraphAPI
      .getSubjectGraph(subjectId)
      .then((response) => {
        const data = response.data;
        setGraph(data);

        // 验证图谱是否为空（无章节）
        if (data.chapters.length === 0) {
          setError('该学科暂无知识图谱数据');
        }
      })
      .catch((err: unknown) => {
        let message = '加载知识图谱失败，请稍后重试';
        if (axios.isAxiosError(err)) {
          const status = err.response?.status;
          if (status === 404) {
            message = '该学科暂无知识图谱数据';
          } else {
            const detail = err.response?.data?.detail;
            if (typeof detail === 'string') message = detail;
          }
        }
        setError(message);
      })
      .finally(() => {
        setIsLoadingGraph(false);
      });
  }, []);

  useEffect(() => {
    fetchGraph(selectedSubjectId);
  }, [selectedSubjectId, fetchGraph]);

  // 加载掌握度
  useEffect(() => {
    if (!selectedChildId || !selectedSubjectId) return;

    knowledgeGraphAPI
      .getChildMastery(selectedChildId, selectedSubjectId)
      .then((response) => {
        const map: Record<string, number> = {};
        response.data.forEach((entry) => {
          map[entry.kp_id] = entry.mastery_score;
        });
        setMasteryMap(map);
      })
      .catch(() => {
        // 掌握度加载失败不妨碍图谱显示
      });
  }, [selectedChildId, selectedSubjectId]);

  // 初始化数学图谱
  const handleInitMathGraph = async () => {
    setIsInitLoading(true);
    setError('');

    try {
      await knowledgeGraphAPI.initMathGraph();
      await fetchSubjects();
      setSelectedSubjectId('math');
    } catch (err: unknown) {
      let message = '初始化失败，请稍后重试';
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') message = detail;
      }
      setError(message);
    } finally {
      setIsInitLoading(false);
    }
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
        <h1 className="text-2xl font-bold text-gray-800">知识图谱</h1>

        {/* 选择器区域 */}
        <div className="bg-white rounded-lg shadow p-4 flex flex-wrap gap-4 items-end">
          {/* 孩子选择 */}
          {user.children.length > 0 && (
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
          )}

          {/* 学科选择 */}
          {subjects.length > 0 && (
            <div>
              <label className="block text-sm text-gray-600 mb-1">学科</label>
              <div className="flex gap-2">
                {subjects.map((subject) => (
                  <button
                    key={subject.id}
                    onClick={() => setSelectedSubjectId(subject.id)}
                    className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                      selectedSubjectId === subject.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {subject.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* 初始化数学图谱按钮 */}
          {(!isLoadingSubjects && subjects.length === 0 && !error) || (
            <button
              type="button"
              onClick={handleInitMathGraph}
              disabled={isInitLoading}
              className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isInitLoading ? '初始化中...' : '初始化数学图谱'}
            </button>
          )}
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm flex justify-between items-center">
            <span>{error}</span>
            <div className="flex gap-2">
              {graph && (
                <button
                  type="button"
                  onClick={() => fetchGraph(selectedSubjectId)}
                  className="px-3 py-1 border border-red-300 rounded hover:bg-red-100 transition-colors"
                >
                  重试
                </button>
              )}
              {subjects.length === 0 && (
                <button
                  type="button"
                  onClick={handleInitMathGraph}
                  disabled={isInitLoading}
                  className="px-3 py-1 border border-green-300 rounded hover:bg-green-100 transition-colors disabled:opacity-50"
                >
                  {isInitLoading ? '初始化中...' : '初始化数学图谱'}
                </button>
              )}
            </div>
          </div>
        )}

        {/* 加载中 */}
        {isLoadingSubjects && (
          <div className="flex justify-center items-center h-64">
            <span className="text-gray-500">加载学科列表...</span>
          </div>
        )}

        {isLoadingGraph && !isLoadingSubjects && (
          <div className="flex justify-center items-center h-64">
            <span className="text-gray-500">加载知识图谱...</span>
          </div>
        )}

        {/* 图谱内容 */}
        {!isLoadingGraph && !isLoadingSubjects && graph && graph.chapters.length > 0 && (
          <GraphCanvas graph={graph} masteryMap={masteryMap} />
        )}

        {/* 空状态 */}
        {!isLoadingGraph && !isLoadingSubjects && !graph && !error && subjects.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-white rounded-lg shadow">
            <p className="mb-4">暂无知识图谱数据</p>
            <button
              type="button"
              onClick={handleInitMathGraph}
              disabled={isInitLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {isInitLoading ? '初始化中...' : '初始化数学知识图谱'}
            </button>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default KnowledgeGraphPage;
