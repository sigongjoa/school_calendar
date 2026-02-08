import api from './api';
import { School, SchoolSearchResult } from '../types';

export const schoolApi = {
    // Get all schools
    getAll: async (): Promise<School[]> => {
        const response = await api.get<School[]>('/schools');
        return response.data;
    },

    // Create school
    create: async (data: any): Promise<School> => {
        // Types are loosely typed in frontend input often, but response is strict
        const response = await api.post<School>('/schools', data);
        return response.data;
    },

    // Update school
    update: async (id: number, data: Partial<School>): Promise<School> => {
        const response = await api.patch<School>(`/schools/${id}`, data);
        return response.data;
    },

    // Delete school
    delete: async (id: number): Promise<void> => {
        await api.delete(`/schools/${id}`);
    },

    // Search schools via NEIS (Proxy)
    search: async (keyword: string): Promise<SchoolSearchResult[]> => {
        const response = await api.get<SchoolSearchResult[]>('/schools/search', {
            params: { keyword },
        });
        return response.data;
    },
};
