import { create } from 'zustand';
import { School } from '../types';
import { schoolApi } from '../services/schoolApi';

interface SchoolStore {
    schools: School[];
    isLoading: boolean;
    error: string | null;

    fetchSchools: () => Promise<void>;
    addSchool: (school: School) => void;
    updateSchool: (id: number, updates: Partial<School>) => void; // local update
    removeSchool: (id: number) => void; // local remove
    toggleSchool: (id: number) => Promise<void>;
}

export const useSchoolStore = create<SchoolStore>((set) => ({
    schools: [],
    isLoading: false,
    error: null,

    fetchSchools: async () => {
        set({ isLoading: true, error: null });
        try {
            const schools = await schoolApi.getAll();
            set({ schools });
        } catch (err) {
            // Casting err to any or specific error type
            set({ error: 'Failed to fetch schools' });
            console.error(err);
        } finally {
            set({ isLoading: false });
        }
    },

    addSchool: (school: School) => {
        set((state: any) => ({ schools: [...state.schools, school] }));
    },

    updateSchool: (id: number, updates: Partial<School>) => {
        set((state: any) => ({
            schools: state.schools.map((s: any) => (s.id === id ? { ...s, ...updates } : s)),
        }));
    },

    removeSchool: (id: number) => {
        set((state: any) => ({
            schools: state.schools.filter((s: any) => s.id !== id),
        }));
    },

    toggleSchool: async (id: number) => {
        const school = useSchoolStore.getState().schools.find((s) => s.id === id);
        if (!school) return;

        const newEnabled = !school.enabled;
        // Optimistic update
        useSchoolStore.getState().updateSchool(id, { enabled: newEnabled });

        try {
            await schoolApi.update(id, { enabled: newEnabled });
        } catch (err) {
            // Revert on fail
            useSchoolStore.getState().updateSchool(id, { enabled: !newEnabled });
            console.error(err);
        }
    },
}));
