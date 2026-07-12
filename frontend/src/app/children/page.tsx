'use client';

import React, { useCallback, useEffect, useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { useAuth } from '@/hooks/useAuth';
import { childrenAPI } from '@/lib/api';
import { Child } from '@/types';
import axios from 'axios';

/**
 * 年级选项（7-12 对应初一至高三）
 */
const GRADE_OPTIONS: { value: number; label: string }[] = [
  { value: 7, label: '初一' },
  { value: 8, label: '初二' },
  { value: 9, label: '初三' },
  { value: 10, label: '高一' },
  { value: 11, label: '高二' },
  { value: 12, label: '高三' },
];

/**
 * 科目选项
 */
const SUBJECT_OPTIONS = ['数学', '物理', '化学', '英语'];

/**
 * 将年级数值转换为中文标签
 */
const getGradeLabel = (grade: number): string => {
  const option = GRADE_OPTIONS.find((item) => item.value === grade);
  return option ? option.label : `年级 ${grade}`;
};

/**
 * 格式化日期字符串
 */
const formatDate = (dateString?: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('zh-CN');
};

const ChildrenPage: React.FC = () => {
  const { user, isLoading: isAuthLoading } = useAuth();

  const [children, setChildren] = useState<Child[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [listError, setListError] = useState('');
  const [formError, setFormError] = useState('');

  const [name, setName] = useState('');
  const [grade, setGrade] = useState<number>(7);
  const [subjects, setSubjects] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * 拉取孩子列表
   */
  const fetchChildren = useCallback(() => {
    setIsLoading(true);
    setListError('');

    childrenAPI
      .getChildren()
      .then((response) => {
        setChildren(response.data || []);
      })
      .catch((err: unknown) => {
        let message = '加载孩子列表失败，请稍后重试';
        if (axios.isAxiosError(err)) {
          const detail = err.response?.data?.detail;
          if (typeof detail === 'string') {
            message = detail;
          }
        }
        setListError(message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  useEffect(() => {
    if (user) {
      fetchChildren();
    }
  }, [user, fetchChildren]);

  /**
   * 切换科目选中状态
   */
  const toggleSubject = (subject: string) => {
    setSubjects((prev) =>
      prev.includes(subject) ? prev.filter((s) => s !== subject) : [...prev, subject]
    );
  };

  /**
   * 重置表单
   */
  const resetForm = () => {
    setName('');
    setGrade(7);
    setSubjects([]);
    setFormError('');
  };

  /**
   * 提交添加孩子表单
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    if (!name.trim()) {
      setFormError('请输入孩子姓名');
      return;
    }

    setIsSubmitting(true);

    try {
      await childrenAPI.createChild({
        name: name.trim(),
        grade,
        subjects,
      });
      resetForm();
      fetchChildren();
    } catch (err: unknown) {
      let message = '添加失败，请稍后重试';
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          message = detail;
        } else if (Array.isArray(detail)) {
          message = detail.map((item: { msg?: string }) => item.msg || JSON.stringify(item)).join('；');
        }
      }
      setFormError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * 删除孩子
   */
  const handleDelete = async (childId: string) => {
    if (!window.confirm('确定删除该孩子吗？相关错题和试卷数据可能受到影响。')) {
      return;
    }

    try {
      await childrenAPI.deleteChild(childId);
      fetchChildren();
    } catch (err: unknown) {
      let message = '删除失败，请稍后重试';
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          message = detail;
        }
      }
      setListError(message);
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
        <h1 className="text-2xl font-bold text-gray-800">孩子管理</h1>

        {/* 添加孩子表单 */}
        <section className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">添加孩子</h2>

          {formError && (
            <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">{formError}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  姓名 <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="请输入孩子姓名"
                  maxLength={50}
                  className="w-full border rounded-lg px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  年级 <span className="text-red-500">*</span>
                </label>
                <select
                  value={grade}
                  onChange={(e) => setGrade(Number(e.target.value))}
                  className="w-full border rounded-lg px-3 py-2"
                >
                  {GRADE_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">科目</label>
                <div className="flex flex-wrap gap-3 pt-2">
                  {SUBJECT_OPTIONS.map((subject) => (
                    <label key={subject} className="flex items-center space-x-1 text-sm text-gray-700">
                      <input
                        type="checkbox"
                        checked={subjects.includes(subject)}
                        onChange={() => toggleSubject(subject)}
                        className="rounded border-gray-300"
                      />
                      <span>{subject}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? '添加中...' : '添加'}
              </button>
            </div>
          </form>
        </section>

        {/* 孩子列表 */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">孩子列表</h2>

          {isLoading && (
            <div className="flex justify-center items-center h-64">
              <span className="text-gray-500">加载中...</span>
            </div>
          )}

          {listError && !isLoading && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm flex justify-between items-center">
              <span>{listError}</span>
              <button
                type="button"
                onClick={fetchChildren}
                className="px-3 py-1 border border-red-300 rounded hover:bg-red-100 transition-colors"
              >
                重试
              </button>
            </div>
          )}

          {!isLoading && !listError && children.length === 0 && (
            <div className="text-center py-12 text-gray-500 bg-white rounded-lg shadow">
              暂无孩子，请添加一个孩子
            </div>
          )}

          {!isLoading && !listError && children.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {children.map((child) => (
                <div
                  key={child.id}
                  className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-800">{child.name}</h3>
                      <span className="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                        {getGradeLabel(child.grade)}
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleDelete(child.id)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      删除
                    </button>
                  </div>

                  {child.subjects && child.subjects.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {child.subjects.map((subject) => (
                        <span
                          key={subject}
                          className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700"
                        >
                          {subject}
                        </span>
                      ))}
                    </div>
                  )}

                  <div className="text-xs text-gray-400">
                    创建时间：{formatDate(child.created_at)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </MainLayout>
  );
};

export default ChildrenPage;
