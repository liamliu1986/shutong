/**
 * 全局 TypeScript 类型定义
 */

/**
 * 用户信息
 */
export interface User {
  id: string;
  username: string;
  email: string;
  children: Child[];
}

/**
 * 孩子信息
 */
export interface Child {
  id: string;
  name: string;
  grade: number;
  subjects: string[];
  created_at?: string;
}

/**
 * 知识点
 */
export interface KnowledgePoint {
  id: string;
  name: string;
  description?: string;
  order?: number;
}

/**
 * 错题记录
 */
export interface Mistake {
  id: string;
  child_id: string;
  subject: string;
  grade?: string;
  chapter: string;
  knowledge_points: string[];
  question_image_url: string;
  question_text: string;
  question_latex: string;
  answer: string;
  explanation: string;
  explanation_gif_url: string;
  difficulty: number;
  source: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

/**
 * 题目选项
 */
export interface QuestionOption {
  label: string;
  content: string;
  is_correct: boolean;
}

/**
 * 题库题目
 */
export interface Question {
  id: string;
  child_id: string;
  subject: string;
  grade: number;
  question_type: "choice" | "fill_blank" | "solve";
  question_text: string;
  question_latex: string;
  question_image_url: string;
  options: QuestionOption[];
  answer: string;
  explanation: string;
  chapter: string;
  knowledge_point_ids: string[];
  difficulty: number;
  tags: string[];
  source_type: "single" | "paper";
  source_paper_id?: string;
  source_paper_name?: string;
  question_index?: number;
  used_count: number;
  correct_rate: number;
  created_at: string;
  updated_at: string;
}

/**
 * 试卷
 */
export interface Paper {
  id: string;
  child_id: string;
  name: string;
  subject: string;
  grade: number;
  images: { url: string; name?: string }[];
  question_ids: string[];
  question_count: number;
  source: string;
  exam_date?: string;
  total_score?: number;
  status: "uploaded" | "processing" | "completed" | "failed";
  created_at: string;
}

/**
 * 自由组卷配置
 */
export interface GeneratePaperConfig {
  child_id: string;
  subject: string;
  grade: number;
  chapter?: string;
  knowledge_point_ids?: string[];
  question_count: number;
  difficulty_distribution?: {
    easy?: number;
    medium?: number;
    hard?: number;
  };
  include_mistakes?: boolean;
}
