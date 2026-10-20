import { useState, useEffect, useCallback } from 'react';
import { Model } from '../types';
import { api } from '../utils/api';
import { getErrorMessage } from '../utils/errorMessage';

const STORAGE_KEY = 'defaultModel';

export function useModels() {
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>(() => {
    return localStorage.getItem(STORAGE_KEY) || '';
  });
  /** W808：加载失败的用户可读文案（null = 无错误）。此前失败只 console.error，模型选择器静默为空。 */
  const [error, setError] = useState<string | null>(null);

  const fetchModels = useCallback(async () => {
    try {
      // W808：改走统一 client——服务端错误不再被当成功数据返回
      const data = await api.models();
      setError(null);

      setModels(data.models ?? []);
      if (data.models?.length > 0 && !selectedModel) {
        const savedDefault = localStorage.getItem(STORAGE_KEY);
        const modelToUse = savedDefault && data.models.some((m: Model) => m.modelId === savedDefault)
          ? savedDefault
          : (data.defaultModel || data.models[0].modelId);
        setSelectedModel(modelToUse);
        localStorage.setItem(STORAGE_KEY, modelToUse);
      }
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, [selectedModel]);

  // 初始加载
  useEffect(() => {
    fetchModels();
  }, []);

  return {
    models,
    selectedModel,
    setSelectedModel,
    fetchModels,
    error,
  };
}
