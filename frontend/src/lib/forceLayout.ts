/**
 * 简单力导向布局引擎
 *
 * 模拟带电粒子间的排斥力和弹簧吸引力，
 * 迭代收敛后产生类似 Obsidian 的自然聚簇布局。
 */

interface ForceNode {
  id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  /** 关联的 chapter id 用于分组力 */
  chapter?: string;
}

interface ForceEdge {
  source: string;
  target: string;
}

/**
 * 计算力导向布局
 * @param nodes 初始节点（需有 id）
 * @param edges 边列表
 * @param width 画布宽度
 * @param height 画布高度
 * @param iterations 迭代次数
 */
export function computeForceLayout(
  nodes: { id: string; chapter?: string }[],
  edges: ForceEdge[],
  width = 1200,
  height = 800,
  iterations = 100
): Map<string, { x: number; y: number }> {
  const fNodes: ForceNode[] = nodes.map((n, i) => {
    // 初始位置：在画布范围内随机分布
    const angle = (2 * Math.PI * i) / nodes.length;
    const radius = Math.min(width, height) * 0.3;
    return {
      id: n.id,
      x: width / 2 + radius * Math.cos(angle),
      y: height / 2 + radius * Math.sin(angle),
      vx: 0,
      vy: 0,
      chapter: n.chapter,
    };
  });

  const nodeMap = new Map<string, ForceNode>();
  fNodes.forEach((n) => nodeMap.set(n.id, n));

  // 构建邻接表
  const adj = new Map<string, Set<string>>();
  fNodes.forEach((n) => adj.set(n.id, new Set()));
  for (const edge of edges) {
    adj.get(edge.source)?.add(edge.target);
    adj.get(edge.target)?.add(edge.source);
  }

  // 同章节点集合
  const chapterGroups = new Map<string, string[]>();
  for (const n of nodes) {
    if (n.chapter) {
      const list = chapterGroups.get(n.chapter) || [];
      list.push(n.id);
      chapterGroups.set(n.chapter, list);
    }
  }

  const area = width * height;
  const k = Math.sqrt(area / fNodes.length); // 理想距离
  const repulsionStrength = k * k * 0.5;
  const attractionStrength = 0.01;
  const chapterAttraction = 0.005; // 同章节吸引力
  const damping = 0.85;
  const minVelocity = 0.1;

  for (let iter = 0; iter < iterations; iter++) {
    // 排斥力（所有节点之间）
    for (let i = 0; i < fNodes.length; i++) {
      for (let j = i + 1; j < fNodes.length; j++) {
        const a = fNodes[i];
        const b = fNodes[j];
        let dx = b.x - a.x;
        let dy = b.y - a.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 1) dist = 1;
        const force = repulsionStrength / (dist * dist);
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        a.vx -= fx;
        a.vy -= fy;
        b.vx += fx;
        b.vy += fy;
      }
    }

    // 吸引力（沿边）
    for (const edge of edges) {
      const a = nodeMap.get(edge.source);
      const b = nodeMap.get(edge.target);
      if (!a || !b) continue;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 1) continue;
      const force = (dist - k) * attractionStrength;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      a.vx += fx;
      a.vy += fy;
      b.vx -= fx;
      b.vy -= fy;
    }

    // 同章节额外吸引力
    chapterGroups.forEach((ids) => {
      for (let i = 0; i < ids.length; i++) {
        for (let j = i + 1; j < ids.length; j++) {
          const a = nodeMap.get(ids[i]);
          const b = nodeMap.get(ids[j]);
          if (!a || !b) continue;
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 1) continue;
          const force = dist * chapterAttraction;
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          a.vx += fx;
          a.vy += fy;
          b.vx -= fx;
          b.vy -= fy;
        }
      }
    });

    // 中心引力（防止飞散）
    for (const n of fNodes) {
      n.vx += (width / 2 - n.x) * 0.001;
      n.vy += (height / 2 - n.y) * 0.001;
    }

    // 更新位置
    for (const n of fNodes) {
      n.vx *= damping;
      n.vy *= damping;
      const speed = Math.sqrt(n.vx * n.vx + n.vy * n.vy);
      if (speed > minVelocity) {
        n.x += n.vx;
        n.y += n.vy;
      }
    }
  }

  // 归一化到画布中心
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const n of fNodes) {
    minX = Math.min(minX, n.x);
    minY = Math.min(minY, n.y);
    maxX = Math.max(maxX, n.x);
    maxY = Math.max(maxY, n.y);
  }
  const rangeX = maxX - minX || 1;
  const rangeY = maxY - minY || 1;
  const scale = Math.min(width * 0.7 / rangeX, height * 0.7 / rangeY);
  const offsetX = (width - rangeX * scale) / 2 - minX * scale;
  const offsetY = (height - rangeY * scale) / 2 - minY * scale;

  const result = new Map<string, { x: number; y: number }>();
  for (const n of fNodes) {
    result.set(n.id, {
      x: n.x * scale + offsetX,
      y: n.y * scale + offsetY,
    });
  }

  return result;
}
