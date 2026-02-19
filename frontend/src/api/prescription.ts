import type { PrescriptionResponse, PrescriptionChatRequest, PrescriptionChatResponse } from './types';
import { useSettingsStore } from '../stores/settingsStore';
import axios from 'axios';

export const analyzePrescription = async (
    file: File,
    onProgress?: (progress: number) => void
): Promise<PrescriptionResponse> => {
    const { apiUrl } = useSettingsStore.getState();
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post<PrescriptionResponse>(
        `${apiUrl}/prescription/analyze`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
                if (onProgress && progressEvent.total) {
                    const progress = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                    onProgress(progress);
                }
            },
            timeout: 180000, // 3 minutes — OCR + search takes time
        }
    );
    return response.data;
};

export const chatAboutPrescription = async (
    request: PrescriptionChatRequest
): Promise<PrescriptionChatResponse> => {
    const { apiUrl } = useSettingsStore.getState();
    const response = await axios.post<PrescriptionChatResponse>(
        `${apiUrl}/prescription/chat`,
        request,
        { timeout: 60000 }
    );
    return response.data;
};
