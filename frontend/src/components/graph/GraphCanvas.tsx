'use client';

import React, { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  type NodeTypes,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import KnowledgePointNode from './KnowledgePointNode';
import type { SubjectGraph, Relation } from '@/types';

// 布局常量
const CHAPTER_GAP = 320; // 章节列间距
const KP_GAP = 130; // 知识点行间距
const CHAPTER_TOP_OFFSET = 60; // 章节标题区域高度
const KP_START_Y = 40; // 第一个知识点的 Y 坐标

// 注册自定义节点类型
const nodeTypes: NodeTypes = {
  knowledgePoint: KnowledgePointNode,
};

/**
 * 将 SubjectGraph 数据转换为 React Flow 节点和边
 */
function buildGraphLayout(
  graph: SubjectGraph,
  masteryMap: Record<string, number>
): { nodes: Node[]; edges: Edge[] } {
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  // 遍历章节，每章为一列
  graph.chapters.forEach((chapter, chapterIndex) => {
    const chapterX = 50 + chapterIndex * CHAPTER_GAP;

    // 章节标题节点（用普通的 PositionNode）
    nodes.push({
      id: `chapter-${chapter.id}`,
      type: 'default',
      position: { x: chapterX, y: 0 },
      data: { label: chapter.name },
      style: {
        background: '#f0f4ff',
        border: '1px solid #bfdbfe',
        borderRadius: '8px',
        padding: '8px 24px',
        fontWeight: 600,
        fontSize: '14px',
        color: '#1e40af',
        width: 200,
        textAlign: 'center' as const,
      },
      draggable: false,
      deletable: false,
      selectable: false,
    });

    // 章节内的知识点节点
    chapter.knowledge_points.forEach((kp, kpIndex) => {
      const kpX = chapterX;
      const kpY = CHAPTER_TOP_OFFSET + kpIndex * KP_GAP;

      nodes.push({
        id: kp.id,
        type: 'knowledgePoint',
        position: { x: kpX, y: kpY },
        data: {
          label: kp.name,
          mastery: masteryMap[kp.id] ?? null,
          importance: kp.importance,
          description: kp.description,
        },
      });
    });
  });

  // 知识点间关系 → 边
  graph.relations.forEach((rel: Relation, index: number) => {
    const isPrerequisite = rel.type === 'PREREQUISITE_OF';

    edges.push({
      id: `edge-${index}`,
      source: rel.from,
      target: rel.to,
      type: 'smoothstep',
      animated: isPrerequisite,
      style: {
        stroke: isPrerequisite ? '#3b82f6' : '#9ca3af',
        strokeWidth: isPrerequisite ? 2 : 1.5,
        strokeDasharray: isPrerequisite ? '5 5' : undefined,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: isPrerequisite ? '#3b82f6' : '#9ca3af',
      },
      label: isPrerequisite ? '前置' : '关联',
      labelStyle: {
        fill: isPrerequisite ? '#3b82f6' : '#9ca3af',
        fontSize: 10,
      },
    });
  });

  return { nodes, edges };
}

interface GraphCanvasProps {
  graph: SubjectGraph;
  masteryMap?: Record<string, number>;
}

/**
 * 知识图谱画布组件
 *
 * 接收 SubjectGraph 数据，渲染为交互式 React Flow 图
 * 支持缩放、平移、小地图预览
 */
const GraphCanvas: React.FC<GraphCanvasProps> = ({ graph, masteryMap = {} }) => {
  const { nodes, edges } = useMemo(
    () => buildGraphLayout(graph, masteryMap),
    [graph, masteryMap]
  );

  return (
    <div className="w-full h-[600px] border rounded-lg bg-white">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.3}
        maxZoom={2}
        attributionPosition="bottom-left"
        className="rounded-lg"
      >
        <Background color="#f3f4f6" gap={20} />
        <Controls className="!shadow-md" />
        <MiniMap
          nodeStrokeColor="#6b7280"
          nodeColor={(node) => {
            if (node.type === 'knowledgePoint') return '#60a5fa';
            return '#bfdbfe';
          }}
          maskColor="rgba(0,0,0,0.1)"
          className="!shadow-md"
        />
      </ReactFlow>
    </div>
  );
};

export default GraphCanvas;
