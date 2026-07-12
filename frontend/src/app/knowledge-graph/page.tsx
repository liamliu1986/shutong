'use client';

import React, { useCallback, useEffect, useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { knowledgeGraphAPI } from '@/lib/api';
import type { Subject, SubjectGraph } from '@/types';
import GraphCanvas from '@/components/graph/GraphCanvas';
import EditPanel from './components/EditPanel';
import AddNodeModal from './components/AddNodeModal';
import axios from 'axios';
import type { Connection } from '@xyflow/react';

/** 编辑面板选中的节点信息 */
interface SelectedNodeInfo {
  id: string;
  type: 'chapter' | 'knowledgePoint';
  name: string;
  description?: string;
  importance?: number;
  order?: number;
  parentChapterId?: string;
}

type AddMode = 'chapter' | 'knowledgePoint' | null;

/**
 * 知识图谱页面
 *
 * 展示学科知识点的交互式关系图，支持编辑模式
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

  // ─── 编辑模式状态 ───
  const [isEditable, setIsEditable] = useState(false);
  const [selectedNode, setSelectedNode] = useState<SelectedNodeInfo | null>(null);
  const [addMode, setAddMode] = useState<AddMode>(null);
  const [selectedKpId, setSelectedKpId] = useState<string | null>(null);

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
    setSelectedNode(null);
    setSelectedKpId(null);

    knowledgeGraphAPI
      .getSubjectGraph(subjectId)
      .then((response) => {
        const data = response.data;
        setGraph(data);
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

  // ─── 编辑模式操作 ───

  /** 切换编辑模式 */
  const toggleEditMode = () => {
    setIsEditable((prev) => !prev);
    setSelectedNode(null);
    setSelectedKpId(null);
  };

  /** 图谱变更后刷新 */
  const refreshGraph = useCallback(() => {
    fetchGraph(selectedSubjectId);
  }, [fetchGraph, selectedSubjectId]);

  /** 知识点点击 → 打开编辑面板 */
  const handleNodeClick = useCallback(
    (nodeId: string) => {
      if (!isEditable || !graph) return;

      if (nodeId.startsWith('chapter-')) {
        const chId = nodeId.replace('chapter-', '');
        const chapter = graph.chapters.find((c) => c.id === chId);
        if (chapter) {
          setSelectedNode({
            id: chId,
            type: 'chapter',
            name: chapter.name,
            order: chapter.order,
          });
          setSelectedKpId(null);
        }
      } else {
        for (const ch of graph.chapters) {
          const kp = ch.knowledge_points.find((k) => k.id === nodeId);
          if (kp) {
            setSelectedNode({
              id: kp.id,
              type: 'knowledgePoint',
              name: kp.name,
              description: kp.description,
              importance: kp.importance,
              parentChapterId: ch.id,
            });
            setSelectedKpId(kp.id);
            return;
          }
        }
        setSelectedNode(null);
        setSelectedKpId(null);
      }
    },
    [isEditable, graph]
  );

  /** 连接两个知识点 → 创建关系 */
  const handleConnect = useCallback(
    async (connection: Connection) => {
      if (!connection.source || !connection.target) return;

      const relType = window.prompt('关系类型：1=关联(RELATED_TO), 2=前置(PREREQUISITE_OF)', '1');
      const type = relType === '2' ? 'PREREQUISITE_OF' : 'RELATED_TO';

      try {
        await knowledgeGraphAPI.createRelation({
          from_id: connection.source,
          to_id: connection.target,
          type,
        });
        refreshGraph();
      } catch {
        // 忽略错误
      }
    },
    [refreshGraph]
  );

  /** 节点编辑后保存 */
  const handleNodeUpdated = () => {
    refreshGraph();
  };

  /** 节点删除后关闭面板 */
  const handleNodeDeleted = () => {
    setSelectedNode(null);
    setSelectedKpId(null);
    refreshGraph();
  };

  /** 关闭编辑面板 */
  const handleClosePanel = () => {
    setSelectedNode(null);
    setSelectedKpId(null);
  };

  /** 内容变更后刷新（新建后） */
  const handleNodeCreated = () => {
    setAddMode(null);
    refreshGraph();
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
          <h1 className="text-2xl font-bold text-gray-800">知识图谱</h1>

          {/* 编辑模式切换 */}
          {graph && graph.chapters.length > 0 && (
            <button
              type="button"
              onClick={toggleEditMode}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                isEditable
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {isEditable ? '退出编辑' : '编辑图谱'}
            </button>
          )}
        </div>

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
          {!isLoadingSubjects && subjects.length === 0 && !error && (
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

        {/* 图谱内容 + 编辑面板 */}
        {!isLoadingGraph && !isLoadingSubjects && graph && graph.chapters.length > 0 && (
          <div className="flex gap-0">
            {/* 图谱主区域 */}
            <div className="flex-1 min-w-0">
              <GraphCanvas
                graph={graph}
                masteryMap={masteryMap}
                isEditable={isEditable}
                selectedNodeId={selectedKpId}
                onNodeClick={handleNodeClick}
                onConnect={handleConnect}
              />

              {/* 编辑模式浮动工具栏 */}
              {isEditable && (
                <div className="flex gap-2 mt-2">
                  <button
                    type="button"
                    onClick={() => setAddMode('chapter')}
                    className="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors"
                  >
                    + 添加章节
                  </button>
                  <button
                    type="button"
                    onClick={() => setAddMode('knowledgePoint')}
                    className="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors"
                  >
                    + 添加知识点
                  </button>
                </div>
              )}
            </div>

            {/* 编辑侧边栏 */}
            {isEditable && selectedNode && (
              <EditPanel
                selectedNode={selectedNode}
                onClose={handleClosePanel}
                onUpdated={handleNodeUpdated}
                onDeleted={handleNodeDeleted}
              />
            )}
          </div>
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

      {/* 添加节点弹窗 */}
      {addMode && graph && (
        <AddNodeModal
          nodeType={addMode}
          chapters={graph.chapters.map((c) => ({ id: c.id, name: c.name }))}
          subjectId={selectedSubjectId}
          onClose={() => setAddMode(null)}
          onCreated={handleNodeCreated}
        />
      )}
    </MainLayout>
  );
};

export default KnowledgeGraphPage;
