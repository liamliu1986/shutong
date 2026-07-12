'use client';

import React from 'react';
import { Handle, Position, type NodeProps } from '@xyflow/react';

/**
 * 获取掌握度对应的颜色类名
 */
function getMasteryColor(mastery: number | null | undefined): string {
  if (mastery == null) return 'bg-gray-100 border-gray-300';
  if (mastery >= 80) return 'bg-green-100 border-green-500';
  if (mastery >= 60) return 'bg-blue-100 border-blue-500';
  if (mastery >= 40) return 'bg-yellow-100 border-yellow-500';
  return 'bg-red-100 border-red-500';
}

/**
 * 获取掌握度对应的文字颜色
 */
function getMasteryTextColor(mastery: number | null | undefined): string {
  if (mastery == null) return 'text-gray-400';
  if (mastery >= 80) return 'text-green-700';
  if (mastery >= 60) return 'text-blue-700';
  if (mastery >= 40) return 'text-yellow-700';
  return 'text-red-700';
}

/**
 * 知识点节点组件
 *
 * 在知识图谱中渲染单个知识点，显示名称和掌握度
 * 支持连接点（Handles）用于关系连线
 */
const KnowledgePointNode: React.FC<NodeProps> = ({ data }) => {
  const { label, mastery, importance, description } = data;

  return (
    <div
      className={`px-4 py-3 rounded-lg shadow-md border-2 min-w-[160px] ${getMasteryColor(mastery)}`}
    >
      <Handle type="target" position={Position.Top} className="!bg-gray-400" />
      <div className="font-medium text-sm text-gray-800 text-center">{label}</div>
      {description && (
        <div className="text-xs text-gray-500 mt-1 text-center max-w-[200px] leading-tight">
          {description}
        </div>
      )}
      <div className="flex justify-between items-center mt-2">
        {mastery != null && (
          <span className={`text-xs font-medium ${getMasteryTextColor(mastery)}`}>
            掌握度: {Math.round(mastery)}%
          </span>
        )}
        {importance != null && (
          <span className="text-xs text-gray-400">
            {'★'.repeat(Math.min(importance, 5))}
          </span>
        )}
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-gray-400" />
    </div>
  );
};

export default KnowledgePointNode;
