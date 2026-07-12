import axios, { AxiosInstance } from "axios";
import { Mistake, Question, Paper, GeneratePaperConfig, Subject, SubjectGraph, MasteryEntry } from "@/types";

/**
 * API 客户端
 * 所有后端请求都通过此实例发起
 */
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器：自动附加 JWT token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：401 时清除 token 并重定向到登录页
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

/**
 * 认证 API
 */
export const authAPI = {
  register: (data: { username: string; email: string; password: string }) =>
    api.post("/auth/register", data),
  login: (data: { email: string; password: string }) =>
    api.post("/auth/login", data),
  getProfile: () => api.get("/users/me"),
};

/**
 * 孩子管理 API
 */
export const childrenAPI = {
  getChildren: () => api.get("/users/me/children"),
  createChild: (data: { name: string; grade: number; subjects: string[] }) =>
    api.post("/users/me/children", data),
  deleteChild: (childId: string) =>
    api.delete(`/users/me/children/${childId}`),
  getMastery: (childId: string, subjectId: string) =>
    api.get(`/children/${childId}/mastery`, { params: { subject_id: subjectId } }),
};

/**
 * 知识图谱 API
 */
export const knowledgeGraphAPI = {
  getSubjects: () => api.get<Subject[]>("/subjects"),
  getSubjectGraph: (subjectId: string) =>
    api.get<SubjectGraph>(`/subjects/${subjectId}/graph`),
  initMathGraph: () => api.post("/subjects/init-math"),
  getChildMastery: (childId: string, subjectId: string) =>
    api.get<MasteryEntry[]>(`/children/${childId}/mastery`, {
      params: { subject_id: subjectId },
    }),
  refreshMastery: (childId: string, subjectName: string) =>
    api.post(`/children/${childId}/mastery/refresh`, null, {
      params: { subject_name: subjectName },
    }),

  // ─── 学科 CRUD ───
  createSubject: (data: { id: string; name: string; grade_level?: string }) =>
    api.post("/subjects", data),
  updateSubject: (subjectId: string, data: { name?: string; grade_level?: string }) =>
    api.put(`/subjects/${subjectId}`, data),
  deleteSubject: (subjectId: string) =>
    api.delete(`/subjects/${subjectId}`),

  // ─── 章节 CRUD ───
  createChapter: (subjectId: string, data: { id: string; name: string; order: number }) =>
    api.post(`/subjects/${subjectId}/chapters`, data),
  updateChapter: (chapterId: string, data: { name?: string; order?: number }) =>
    api.put(`/chapters/${chapterId}`, data),
  deleteChapter: (chapterId: string) =>
    api.delete(`/chapters/${chapterId}`),

  // ─── 知识点 CRUD ───
  createKnowledgePoint: (chapterId: string, data: {
    id: string; name: string; description?: string; importance?: number
  }) => api.post(`/chapters/${chapterId}/knowledge-points`, data),
  updateKnowledgePoint: (kpId: string, data: {
    name?: string; description?: string; importance?: number
  }) => api.put(`/knowledge-points/${kpId}`, data),
  deleteKnowledgePoint: (kpId: string) =>
    api.delete(`/knowledge-points/${kpId}`),

  // ─── 关系 CRUD ───
  createRelation: (data: { from_id: string; to_id: string; type: string }) =>
    api.post("/relations", data),
  deleteRelation: (fromId: string, toId: string, type: string) =>
    api.delete("/relations", {
      params: { from_id: fromId, to_id: toId, type },
    }),
};

/**
 * 错题本 API
 */
export const mistakesAPI = {
  getMistakes: (params: {
    child_id: string;
    subject?: string;
    chapter?: string;
    page?: number;
    page_size?: number;
  }) => api.get("/mistakes", { params }),
  getMistake: (id: string) => api.get(`/mistakes/${id}`),
  createMistake: (data: Omit<Mistake, "id" | "created_at" | "updated_at">) =>
    api.post("/mistakes", data),
  updateMistake: (id: string, data: Partial<Mistake>) =>
    api.put(`/mistakes/${id}`, data),
  deleteMistake: (id: string) => api.delete(`/mistakes/${id}`),
  getExplanation: (id: string) => api.get(`/mistakes/${id}/explanation`),
};

/**
 * 题库 API
 */
export const questionBankAPI = {
  getQuestions: (params: {
    child_id: string;
    subject?: string;
    question_type?: string;
    difficulty?: number;
    page?: number;
    page_size?: number;
  }) => api.get("/question-bank", { params }),
  getQuestion: (id: string) => api.get(`/question-bank/${id}`),
  createQuestion: (data: Omit<Question, "id" | "created_at" | "updated_at">) =>
    api.post("/question-bank", data),
  deleteQuestion: (id: string) => api.delete(`/question-bank/${id}`),
};

/**
 * 试卷 API
 */
export const papersAPI = {
  getPapers: (params: { child_id: string }) => api.get("/papers", { params }),
  getPaper: (id: string) => api.get(`/papers/${id}`),
  createPaper: (data: Omit<Paper, "id" | "created_at">) =>
    api.post("/papers", data),
  deletePaper: (id: string) => api.delete(`/papers/${id}`),
  recognizePaper: (id: string) => api.post(`/papers/${id}/recognize`),
};

/**
 * 自由组卷 API
 */
export const generatePaperAPI = {
  generate: (config: GeneratePaperConfig) =>
    api.post("/generate-paper", config),
};

export default api;
