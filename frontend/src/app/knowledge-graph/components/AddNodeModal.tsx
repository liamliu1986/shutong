'use client';

import React, { useState } from 'react';
import { knowledgeGraphAPI } from '@/lib/api';

interface Chapter {
  id: string;
  name: string;
}

type NodeType = 'chapter' | 'knowledgePoint';

interface AddNodeModalProps {
  nodeType: NodeType;
  chapters: Chapter[];
  subjectId: string;
  onClose: () => void;
  onCreated: () => void;
}

/**
 * 添加节点弹窗
 *
 * 支持添加章节和知识点
 */
const AddNodeModal: React.FC<AddNodeModalProps> = ({
  nodeType,
  chapters,
  subjectId,
  onClose,
  onCreated,
}) => {
  const [id, setId] = useState('');
  const [name, setName] = useState('');
  const [order, setOrder] = useState(chapters.length + 1);
  const [description, setDescription] = useState('');
  const [importance, setImportance] = useState(3);
  const [selectedChapterId, setSelectedChapterId] = useState(
    chapters.length > 0 ? chapters[0].id : ''
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const isChapter = nodeType === 'chapter';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!id.trim()) {
      setError('标识不能为空');
      return;
    }
    if (!name.trim()) {
      setError('名称不能为空');
      return;
    }
    if (!isChapter && !selectedChapterId) {
      setError('请选择所属章节');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      if (isChapter) {
        await knowledgeGraphAPI.createChapter(subjectId, {
          id: id.trim(),
          name: name.trim(),
          order,
        });
      } else {
        await knowledgeGraphAPI.createKnowledgePoint(selectedChapterId, {
          id: id.trim(),
          name: name.trim(),
          description: description.trim() || undefined,
          importance,
        });
      }
      onCreated();
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        setError(axiosErr.response?.data?.detail || '创建失败，请重试');
      } else {
        setError('创建失败，请重试');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md mx-4 p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">
            添加{isChapter ? '章节' : '知识点'}
          </h3>
          <button
            type="button"
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {error && (
            <div className="bg-red-50 text-red-600 p-2 rounded text-sm">
              {error}
            </div>
          )}

          {/* ID 标识 */}
          <div>
            <label className="block text-sm text-gray-600 mb-1">
              标识 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={id}
              onChange={(e) => setId(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder={`如 ${isChapter ? 'ch5' : 'kp13'}`}
              required
            />
          </div>

          {/* 名称 */}
          <div>
            <label className="block text-sm text-gray-600 mb-1">
              名称 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="输入名称"
              required
            />
          </div>

          {/* 排序（章节） */}
          {isChapter && (
            <div>
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

          {/* 所属章节（知识点） */}
          {!isChapter && (
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                所属章节 <span className="text-red-500">*</span>
              </label>
              <select
                value={selectedChapterId}
                onChange={(e) => setSelectedChapterId(e.target.value)}
                className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              >
                {chapters.map((ch) => (
                  <option key={ch.id} value={ch.id}>
                    {ch.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* 描述（知识点） */}
          {!isChapter && (
            <>
              <div>
                <label className="block text-sm text-gray-600 mb-1">描述</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                  rows={2}
                  placeholder="知识点描述（可选）"
                />
              </div>

              {/* 重要度 */}
              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  重要度（{importance}）
                </label>
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setImportance(star)}
                      className={`text-xl ${
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

          {/* 提交按钮 */}
          <div className="flex gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-3 py-2 border border-gray-300 text-gray-700 text-sm rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-3 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              {isSubmitting ? '创建中...' : '创建'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddNodeModal;
