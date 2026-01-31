import { apiClient, uploadFileWithProgress } from './client';
import type { UploadResponse, ProcessRequest, ProcessResponse } from './types';

export const uploadFile = async (
    projectId: number,
    file: File,
    onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
    const response = await uploadFileWithProgress(
        `/data/upload/${projectId}`,
        file,
        onProgress
    );
    return response.data;
};

export const processFiles = async (
    projectId: number,
    request: ProcessRequest
): Promise<ProcessResponse> => {
    const response = await apiClient.post<ProcessResponse>(
        `/data/process/${projectId}`,
        request
    );
    return response.data;
};
