'use client';

import React, { useMemo, useCallback, useEffect, useState, useRef } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  type NodeTypes,
  type Connection,
  type OnNodesChange,
  MarkerType,
  SelectionMode,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import KnowledgePointNode from './KnowledgePointNode';
import type { SubjectGraph, Relation } from '@/types';
import { computeForceLayout } from '@/lib/forceLayout';
import { knowledgeGraphAPI } from '@/lib/api';

// 注册自定义节点类型
const nodeTypes: NodeTypes = {
  knowledgePoint: KnowledgePointNode,
};

interface GraphCanvasProps {
  graph: SubjectGraph;
  masteryMap?: Record<string, number>;
  isEditable?: boolean;
  selectedNodeId?: string | null;
  onNodeClick?: (nodeId: string) => void;
  onConnect?: (connection: Connection) => void;
}

/**
 * 知识图谱画布组件
 *
 * 使用力导向布局（Obsidian 风格），支持自由拖拽和连线
 */
const GraphCanvas: React.FC<GraphCanvasProps> = ({
  graph,
  masteryMap = {},
  isEditable = false,
  selectedNodeId,
  onNodeClick,
  onConnect,
}) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [layoutReady, setLayoutReady] = useState(false);
  const saveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // 构建力和存储的混合布局
  useEffect(() => {
    if (!graph || graph.chapters.length === 0) return;

    // 检查知识点是否有已存储的位置
    const hasStoredPositions = graph.chapters.some((ch) =>
      ch.knowledge_points.some((kp) => kp.pos_x !== 0 || kp.pos_y !== 0)
    );

    // 构建力导向布局节点
    const forceNodes = graph.chapters.flatMap((ch) =>
      ch.knowledge_points.map((kp) => ({
        id: kp.id,
        chapter: ch.id,
      }))
    );

    // 构建边
    const forceEdges = graph.relations.map((rel) => ({
      source: rel.from_id,
      target: rel.to_id,
    }));

    // 计算力导向布局位置
    const canvasWidth = 1200;
    const canvasHeight = 600;
    const forcePositions = computeForceLayout(
      forceNodes,
      forceEdges,
      canvasWidth,
      canvasHeight,
      80
    );

    // 生成 React Flow 节点
    const newNodes: Node[] = [];
    let kpIndex = 0;

    graph.chapters.forEach((chapter) => {
      // 章节标签（用普通节点 + 特殊样式）
      const chapterNodeId = `chapter-${chapter.id}`;
      const firstKp = chapter.knowledge_points[0];
      const kpPosX = firstKp?.pos_x ?? 0;
      const kpPosY = firstKp?.pos_y ?? 0;
      const forcePos = firstKp ? forcePositions.get(firstKp.id) : undefined;
      let chX = 0, chY = -60;
      if (hasStoredPositions && (kpPosX !== 0 || kpPosY !== 0)) {
        chX = kpPosX;
        chY = kpPosY - 60;
      } else if (forcePos) {
        chX = forcePos.x;
        chY = forcePos.y - 20;
      }

      newNodes.push({
        id: chapterNodeId,
        type: 'default',
        position: { x: chX - 100, y: chY },
        data: { label: chapter.name },
        style: {
          background: '#e8f0fe',
          border: '1px solid #a8c7fa',
          borderRadius: '20px',
          padding: '4px 16px',
          fontWeight: 600,
          fontSize: '13px',
          color: '#1a56db',
          width: 'auto',
          textAlign: 'center' as const,
        },
        draggable: false,
        deletable: false,
        selectable: false,
      });

      // 知识点节点
      chapter.knowledge_points.forEach((kp) => {
        let pos: { x: number; y: number };

        const kpX = kp.pos_x ?? 0;
        const kpY = kp.pos_y ?? 0;
        if (hasStoredPositions && (kpX !== 0 || kpY !== 0)) {
          // 使用存储的位置
          pos = { x: kpX, y: kpY };
        } else {
          // 使用力导向布局位置
          const fp = forcePositions.get(kp.id);
          if (fp) {
            pos = {
              x: fp.x + (kpIndex % 3 - 1) * 30,
              y: fp.y + Math.floor(kpIndex / 3) * 20,
            };
          } else {
            pos = { x: 200 + kpIndex * 120, y: 200 + (kpIndex % 4) * 100 };
          }
        }

        newNodes.push({
          id: kp.id,
          type: 'knowledgePoint',
          position: pos,
          data: {
            label: kp.name,
            mastery: masteryMap[kp.id] ?? null,
            importance: kp.importance,
            description: kp.description,
          },
        });

        kpIndex++;
      });
    });

    // 构建边
    const newEdges: Edge[] = graph.relations.map((rel: Relation, index: number) => {
      const isPrerequisite = rel.type === 'PREREQUISITE_OF';
      return {
        id: `edge-${index}`,
        source: rel.from_id,
        target: rel.to_id,
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
      };
    });

    setNodes(newNodes);
    setEdges(newEdges);
    setLayoutReady(true);
  }, [graph, masteryMap]);

  // 选择状态同步
  const nodesWithSelection = useMemo(() => {
    if (!selectedNodeId) return nodes;
    return nodes.map((n) => ({
      ...n,
      selected: n.id === selectedNodeId,
    }));
  }, [nodes, selectedNodeId]);

  // 处理节点拖拽结束 → 保存位置
  const handleNodeDragStop = useCallback(
    (_event: MouseEvent | TouchEvent, node: Node) => {
      if (node.id.startsWith('chapter-')) return; // 章节标签不保存

      // 更新本地节点位置
      setNodes((nds) =>
        nds.map((n) =>
          n.id === node.id
            ? { ...n, position: { x: node.position.x, y: node.position.y } }
            : n
        )
      );

      // 防抖批量保存
      if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
      saveTimerRef.current = setTimeout(async () => {
        // 只保存知识点位置（不保存章节标签）
        const kpPositions = nodes
          .filter((n) => !n.id.startsWith('chapter-'))
          .map((n) => ({
            id: n.id,
            x: Math.round(n.position.x),
            y: Math.round(n.position.y),
          }));
        try {
          await knowledgeGraphAPI.savePositions(kpPositions);
        } catch {
          // 位置保存失败不影响图谱显示
        }
      }, 1000);
    },
    [nodes]
  );

  // 节点变化处理（允许自由拖拽）
  const handleNodesChange: OnNodesChange = useCallback((changes) => {
    setNodes((nds) => {
      // 只处理 position 变更
      let updated = [...nds];
      for (const change of changes) {
        if (change.type === 'position' && change.position) {
          updated = updated.map((n) =>
            n.id === change.id
              ? { ...n, position: change.position! }
              : n
          );
        }
      }
      return updated;
    });
  }, []);

  const handleConnect = useCallback(
    (connection: Connection) => {
      if (onConnect) {
        onConnect(connection);
      }
    },
    [onConnect]
  );

  const handleNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      if (onNodeClick && node.type === 'knowledgePoint') {
        onNodeClick(node.id);
      } else if (onNodeClick && node.id.startsWith('chapter-')) {
        const chapterId = node.id.replace('chapter-', '');
        onNodeClick(`chapter-${chapterId}`);
      }
    },
    [onNodeClick]
  );

  if (!layoutReady) {
    return (
      <div className="w-full h-[600px] border rounded-lg bg-white flex items-center justify-center">
        <span className="text-gray-400">布局计算中...</span>
      </div>
    );
  }

  return (
    <div className="w-full h-[600px] border rounded-lg bg-white">
      <ReactFlow
        nodes={nodesWithSelection}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.3}
        maxZoom={2}
        attributionPosition="bottom-left"
        className="rounded-lg"
        nodesDraggable={true}
        nodesConnectable={true}
        elementsSelectable={true}
        selectionMode={SelectionMode.Partial}
        onConnect={handleConnect}
        onNodeClick={handleNodeClick}
        onNodeDragStop={handleNodeDragStop}
        onNodesChange={handleNodesChange}
        deleteKeyCode={isEditable ? 'Backspace' : null}
        multiSelectionKeyCode="Shift"
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
