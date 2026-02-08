import React, { useEffect } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Header } from './components/layout/Header';
import { useSchoolStore } from './stores/useSchoolStore';

import CalendarPage from './pages/CalendarPage';
import SchoolSchedulePage from './pages/SchoolSchedulePage';

function App() {
    const fetchSchools = useSchoolStore((state) => state.fetchSchools);

    useEffect(() => {
        fetchSchools();
    }, [fetchSchools]);

    return (
        <HashRouter>
            <div className="flex flex-col h-screen bg-gray-50">
                <Header />
                <main className="flex-1 overflow-hidden relative">
                    <Routes>
                        <Route path="/" element={<CalendarPage />} />
                        <Route path="/schools" element={<SchoolSchedulePage />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </main>
            </div>
        </HashRouter>
    );
}

export default App;
