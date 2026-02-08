import api from './api';
import { SchoolEvent, CalendarResponse, SyncResult } from '../types';

export const scheduleApi = {
    // Get schedules with filters
    getSchedules: async (params: {
        school_id?: number;
        school_ids?: string; // "1,2,3"
        from_date?: string;
        to_date?: string;
        category?: string;
    }): Promise<SchoolEvent[]> => {
        const response = await api.get<SchoolEvent[]>('/schedules', { params });
        return response.data;
    },

    // Get calendar events for a specific month
    getCalendarEvents: async (year: number, month: number): Promise<CalendarResponse> => {
        const response = await api.get<CalendarResponse>('/schedules/calendar', {
            params: { year, month },
        });
        return response.data;
    },

    // Sync specific school
    syncSchool: async (schoolId: number): Promise<SyncResult> => {
        const response = await api.post<SyncResult>(`/schedules/sync/${schoolId}`);
        return response.data;
    },

    // Sync all schools
    syncAll: async () => {
        const response = await api.post('/schedules/sync-all');
        return response.data;
    },
};
