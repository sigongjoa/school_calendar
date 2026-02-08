import { create } from 'zustand';
import { addMonths, subMonths } from 'date-fns';
import { ExamPeriod, SchoolEvent } from '../types';
import { scheduleApi } from '../services/scheduleApi';

interface CalendarStore {
    currentDate: Date; // The reference date for the current view (usually 1st of month)
    viewType: 'month' | 'week' | 'day';

    // Data for the current view
    events: SchoolEvent[];
    examPeriods: ExamPeriod[];
    isLoading: boolean;
    isSyncing: boolean;

    // Actions
    nextMonth: () => void;
    prevMonth: () => void;
    setToday: () => void;
    fetchMonthEvents: () => Promise<void>;
    syncAllSchedules: () => Promise<void>;

    // Ref to refresh
    invalidate: () => Promise<void>;
}

export const useCalendarStore = create<CalendarStore>((set) => ({
    currentDate: new Date(),
    viewType: 'month',
    events: [],
    examPeriods: [],
    isLoading: false,
    isSyncing: false,

    nextMonth: () => {
        set((state) => ({ currentDate: addMonths(state.currentDate, 1) }));
        useCalendarStore.getState().fetchMonthEvents();
    },

    prevMonth: () => {
        set((state: any) => ({ currentDate: subMonths(state.currentDate, 1) }));
        useCalendarStore.getState().fetchMonthEvents();
    },

    setToday: () => {
        set({ currentDate: new Date() });
        useCalendarStore.getState().fetchMonthEvents();
    },

    fetchMonthEvents: async () => {
        const currentDate = useCalendarStore.getState().currentDate;
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth() + 1; // 1-12

        set({ isLoading: true });
        try {
            const data = await scheduleApi.getCalendarEvents(year, month);
            set({
                events: data.events,
                examPeriods: data.exam_periods
            });
        } catch (err) {
            console.error("Failed to fetch calendar events", err);
        } finally {
            set({ isLoading: false });
        }
    },

    syncAllSchedules: async () => {
        set({ isSyncing: true });
        try {
            await scheduleApi.syncAll();
            await useCalendarStore.getState().fetchMonthEvents();
        } catch (err) {
            console.error("Failed to sync all schedules", err);
        } finally {
            set({ isSyncing: false });
        }
    },

    invalidate: async () => {
        await useCalendarStore.getState().fetchMonthEvents();
    }
}));
