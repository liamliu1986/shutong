'use client';

import React, { useState, useEffect } from 'react';
import { knowledgeGraphAPI } from '@/lib/api';

/** 编辑面板选中的节点信息 */
interface SelectedNode {
  id: string;
  type: 'chapter' | 'knowledgePoint';
  name: string;
  description?: string;
  importance?: number;
  order?: number;
  parentChapterId?: string;
}

interface EditPanelProps {
  selectedNode: SelectedNode | null;
  onClose: () => void;
  onUpdated: () => void;  // 刷新图谱
  onDeleted: () => void;  // 刷新图谱
}

/**
 * 知识图谱编辑侧边栏
 *
 * 选中节点后显示编辑表单（名称、描述、重要度、删除按钮）
 */
const EditPanel: React.FC<EditPanelProps> = ({
  selectedNode,
  onClose,
  onUpdated,
  onDeleted,
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [importance, setImportance] = useState(3);
  const [order, setOrder] = useState(1);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (selectedNode) {
      setName(selectedNode.name);
      setDescription(selectedNode.description || '');
      setImportance(selectedNode.importance || 3);
      setOrder(selectedNode.order || 1);
      setError('');
    }
  }, [selectedNode]);

  if (!selectedNode) return null;

  const handleSave = async () => {
    if (!name.trim()) {
      setError('名称不能为空');
      return;
    }

    setIsSaving(true);
    setError('');

    try {
      if (selectedNode.type === 'chapter') {
        await knowledgeGraphAPI.updateChapter(selectedNode.id, {
          name: name.trim(),
          order,
        });
      } else {
        await knowledgeGraphAPI.updateKnowledgePoint(selectedNode.id, {
          name: name.trim(),
          description: description.trim() || undefined,
          importance,
        });
      }
      onUpdated();
    } catch {
      setError('保存失败，请重试');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`确认删除"${selectedNode.name}"？此操作不可撤销。`)) {
      return;
    }

    setIsDeleting(true);
    setError('');

    try {
      if (selectedNode.type === 'chapter') {
        await knowledgeGraphAPI.deleteChapter(selectedNode.id);
      } else {
        await knowledgeGraphAPI.deleteKnowledgePoint(selectedNode.id);
      }
      onDeleted();
    } catch {
      setError('删除失败，请重试');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="w-80 border-l bg-white p-4 overflow-y-auto shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold text-gray-800">
          {selectedNode.type === 'chapter' ? '编辑章节' : '编辑知识点'}
        </h3>
        <button
          type="button"
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 text-xl leading-none"
        >
          &times;
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-2 rounded text-sm mb-3">
          {error}
        </div>
      )}

      {/* 名称 */}
      <div className="mb-3">
        <label className="block text-sm text-gray-600 mb-1">名称</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="输入名称"
        />
      </div>

      {/* 排序（章节） */}
      {selectedNode.type === 'chapter' && (
        <div className="mb-3">
          <label className="block text-sm text-gray-600 mb-1">排序</label>
          <input
            type="number"
            min={1}
            value={order}
            onChange={(e) => setOrder(Number(e.target.value))}
            className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      )}

      {/* 描述（知识点） */}
      {selectedNode.type === 'knowledgePoint' && (
        <>
          <div className="mb-3">
            <label className="block text-sm text-gray-600 mb-1">描述</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              rows={3}
              placeholder="输入知识点描述"
            />
          </div>

          {/* 重要度 */}
          <div className="mb-4">
            <label className="block text-sm text-gray-600 mb-1">
              重要度（{importance}）
            </label>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setImportance(star)}
                  className={`text-lg ${
                    star <= importance
                      ? 'text-yellow-500'
                      : 'text-gray-300'
                  }`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
        </>
      )}

      {/* 操作按钮 */}
      <div className="flex gap-2 mt-4">
        <button
          type="button"
          onClick={handleSave}
          disabled={isSaving}
          className="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {isSaving ? '保存中...' : '保存'}
        </button>
        <button
          type="button"
          onClick={handleDelete}
          disabled={isDeleting}
          className="px-3 py-2 bg-red-500 text-white text-sm rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50"
        >
          {isDeleting ? '删除中...' : '删除'}
        </button>
      </div>
    </div>
  );
};

export default EditPanel;
