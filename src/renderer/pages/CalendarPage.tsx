import React, { useState, useMemo, useEffect } from 'react';
import {
    format,
    addMonths,
    subMonths,
    startOfMonth,
    endOfMonth,
    startOfWeek,
    endOfWeek,
    eachDayOfInterval,
    isSameMonth,
    isSameDay,
    isToday,
    getDay,
} from 'date-fns';
import { ko } from 'date-fns/locale';
import { ChevronLeft, ChevronRight, Filter, Download, Building2, RefreshCcw } from 'lucide-react';
import clsx from 'clsx';
import { CATEGORY_CONFIG, EventCategory } from '../types';
import { useSchoolStore } from '../stores/useSchoolStore';
import { useCalendarStore } from '../stores/useCalendarStore';

const CalendarPage: React.FC = () => {
    const { schools, fetchSchools } = useSchoolStore();
    const {
        currentDate, nextMonth, prevMonth, setToday,
        events, fetchMonthEvents, syncAllSchedules, isSyncing
    } = useCalendarStore();

    // Toggled school IDs for filtering
    const [visibleSchoolIds, setVisibleSchoolIds] = useState<Set<number>>(new Set());

    useEffect(() => {
        fetchSchools();
        fetchMonthEvents();
    }, []);

    // Initialize all schools as visible when they load
    useEffect(() => {
        if (schools.length > 0 && visibleSchoolIds.size === 0) {
            setVisibleSchoolIds(new Set(schools.map(s => s.id)));
        }
    }, [schools]);

    const toggleSchoolVisibility = (id: number) => {
        const next = new Set(visibleSchoolIds);
        if (next.has(id)) {
            next.delete(id);
        } else {
            next.add(id);
        }
        setVisibleSchoolIds(next);
    };

    const days = useMemo(() => {
        const monthStart = startOfMonth(currentDate);
        const monthEnd = endOfMonth(monthStart);
        const startDate = startOfWeek(monthStart);
        const endDate = endOfWeek(monthEnd);

        return eachDayOfInterval({ start: startDate, end: endDate });
    }, [currentDate]);

    const getEventsForDay = (day: Date) => {
        return events.filter(event =>
            isSameDay(new Date(event.date), day) &&
            visibleSchoolIds.has(event.school_id)
        );
    };

    const weekDays = ['일', '월', '화', '수', '목', '금', '토'];

    return (
        <div className="h-full flex flex-col p-6 animate-in fade-in duration-500 overflow-hidden">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                    <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">
                        {format(currentDate, 'yyyy년 MMMM', { locale: ko })}
                    </h2>
                    <p className="text-gray-500 mt-1">구독 중인 학교 일정을 확인하세요.</p>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex bg-white rounded-xl shadow-sm border p-1">
                        <button
                            onClick={prevMonth}
                            className="p-2 hover:bg-gray-50 rounded-lg transition-colors text-gray-600"
                        >
                            <ChevronLeft className="w-5 h-5" />
                        </button>
                        <button
                            onClick={setToday}
                            className="px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 rounded-lg"
                        >
                            오늘
                        </button>
                        <button
                            onClick={nextMonth}
                            className="p-2 hover:bg-gray-50 rounded-lg transition-colors text-gray-600"
                        >
                            <ChevronRight className="w-5 h-5" />
                        </button>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={syncAllSchedules}
                            disabled={isSyncing}
                            className={clsx(
                                "flex items-center gap-2 px-4 py-2 bg-white border rounded-xl shadow-sm text-sm font-semibold transition-all active:scale-95 disabled:opacity-50",
                                isSyncing ? "text-indigo-400" : "text-gray-700 hover:bg-gray-50"
                            )}
                        >
                            <RefreshCcw className={clsx("w-4 h-4", isSyncing && "animate-spin")} />
                            월별 업데이트
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl shadow-md hover:bg-indigo-700 transition-all active:scale-95 text-sm font-semibold">
                            <Download className="w-4 h-4" />
                            내보내기
                        </button>
                    </div>
                </div>
            </div>

            {/* School Toggles */}
            <div className="flex flex-wrap gap-2 mb-6 p-2 bg-gray-50/50 rounded-2xl border border-gray-100">
                {schools.map(school => (
                    <button
                        key={school.id}
                        onClick={() => toggleSchoolVisibility(school.id)}
                        className={clsx(
                            "flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold transition-all border-2",
                            visibleSchoolIds.has(school.id)
                                ? "bg-white border-transparent text-gray-800 shadow-sm"
                                : "bg-transparent border-gray-200 text-gray-400 grayscale"
                        )}
                        style={{
                            borderLeftColor: visibleSchoolIds.has(school.id) ? school.color : undefined,
                            borderLeftWidth: visibleSchoolIds.has(school.id) ? '4px' : undefined
                        }}
                    >
                        <Building2 className="w-4 h-4" style={{ color: visibleSchoolIds.has(school.id) ? school.color : undefined }} />
                        {school.name}
                    </button>
                ))}
            </div>

            {/* Calendar Grid */}
            <div className="flex-1 bg-white rounded-3xl border border-gray-200 shadow-xl overflow-hidden flex flex-col">
                {/* Weekday Header */}
                <div className="grid grid-cols-7 border-b bg-gray-50/80 backdrop-blur-sm">
                    {weekDays.map((day, idx) => (
                        <div
                            key={day}
                            className={clsx(
                                "py-4 text-center text-xs font-bold uppercase tracking-widest border-r last:border-r-0 border-gray-100",
                                idx === 0 ? "text-red-500" : idx === 6 ? "text-blue-500" : "text-gray-400"
                            )}
                        >
                            {day}
                        </div>
                    ))}
                </div>

                {/* Days Grid */}
                <div className="flex-1 grid grid-cols-7 auto-rows-fr">
                    {days.map((day) => {
                        const dayEvents = getEventsForDay(day);
                        const isSelectedMonth = isSameMonth(day, currentDate);
                        const isTodayDay = isToday(day);
                        const isSun = getDay(day) === 0;
                        const isSat = getDay(day) === 6;

                        return (
                            <div
                                key={day.toString()}
                                className={clsx(
                                    "relative group min-h-[100px] p-2 border-r border-b hover:bg-gray-50/50 transition-colors cursor-pointer last:border-r-0 border-gray-100",
                                    !isSelectedMonth && "bg-gray-50/30 text-gray-300"
                                )}
                            >
                                <div className="flex items-start justify-between">
                                    <span className={clsx(
                                        "inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold transition-all",
                                        isTodayDay ? "bg-indigo-600 text-white shadow-lg shadow-indigo-200" :
                                            isSun ? "text-red-500" :
                                                isSat ? "text-blue-400" : "text-gray-700",
                                        !isSelectedMonth && "text-gray-300"
                                    )}>
                                        {format(day, 'd')}
                                    </span>
                                </div>

                                <div className="mt-2 space-y-1 overflow-hidden">
                                    {dayEvents.map(event => (
                                        <div
                                            key={event.id}
                                            className="px-2 py-1 rounded text-[11px] font-bold truncate transition-all hover:scale-[1.02] text-white shadow-sm"
                                            style={{ backgroundColor: event.school_color || '#4f46e5' }}
                                            title={`${event.school_name}: ${event.title}`}
                                        >
                                            {event.title}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default CalendarPage;
