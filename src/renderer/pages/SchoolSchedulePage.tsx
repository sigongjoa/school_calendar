import React, { useState } from 'react';
import { Search, Building2, Plus, RefreshCw, Trash2, CheckCircle2, Settings2 } from 'lucide-react';
import { School } from '../types';

// Mock Data for Schools
const MOCK_REGISTERED_SCHOOLS: Partial<School>[] = [
    { id: 1, name: '대치고등학교', atpt_code: 'B10', sd_code: '7010057', school_type: 'high', color: '#4f46e5', enabled: true, last_sync_at: '2026-02-06T09:00:00Z', event_count: 42 },
    { id: 2, name: '역삼중학교', atpt_code: 'B10', sd_code: '7010569', school_type: 'middle', color: '#10b981', enabled: true, last_sync_at: '2026-02-05T14:30:00Z', event_count: 28 },
];

const MOCK_SEARCH_RESULTS = [
    { name: '시지중학교', address: '대구광역시 수성구 시지로 10', atpt_code: 'R10', sd_code: '8311025' },
    { name: '시지고등학교', address: '대구광역시 수성구 시지로 20', atpt_code: 'R10', sd_code: '8311026' },
    { name: '노변중학교', address: '대구광역시 수성구 노변로 34', atpt_code: 'R10', sd_code: '8311068' },
    { name: '고산중학교', address: '대구광역시 수성구 고산로 55', atpt_code: 'R10', sd_code: '8311082' },
];

const SchoolSchedulePage: React.FC = () => {
    const [search, setSearch] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [showResults, setShowResults] = useState(false);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSearching(true);
        setTimeout(() => {
            setIsSearching(false);
            setShowResults(true);
        }, 800);
    };

    return (
        <div className="h-full flex flex-col p-6 overflow-y-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Header */}
            <div className="mb-8">
                <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">학교 관리</h2>
                <p className="text-gray-500 mt-1">NEIS 데이터를 구독할 학교를 검색하고 관리하세요.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Search Section */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 relative group overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                            <Search className="w-24 h-24 text-indigo-600" />
                        </div>

                        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                            <Search className="w-5 h-5 text-indigo-500" />
                            학교 검색
                        </h3>

                        <form onSubmit={handleSearch} className="flex gap-2">
                            <div className="relative flex-1">
                                <input
                                    type="text"
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    placeholder="예: 대치고등학교, 7010057..."
                                    className="w-full pl-4 pr-10 py-3 bg-gray-50 border-gray-200 border rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none font-medium"
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={isSearching}
                                className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-indigo-700 transition-all active:scale-95 shadow-lg shadow-indigo-100 flex items-center gap-2"
                            >
                                {isSearching ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                                추가
                            </button>
                        </form>

                        {showResults && (
                            <div className="mt-6 space-y-3 animate-in fade-in zoom-in-95 duration-300">
                                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest pl-1">검색 결과</p>
                                {MOCK_SEARCH_RESULTS.map((res, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors border border-transparent hover:border-gray-200 group">
                                        <div>
                                            <h4 className="font-bold text-gray-800">{res.name}</h4>
                                            <p className="text-sm text-gray-500">{res.address}</p>
                                        </div>
                                        <button className="p-2 bg-white rounded-lg shadow-sm border text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity hover:text-indigo-600 hover:border-indigo-200">
                                            <Plus className="w-5 h-5" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Registered Schools List */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-bold text-gray-800 flex items-center justify-between">
                            구독 중인 학교
                            <span className="text-sm font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded-lg">2개</span>
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {MOCK_REGISTERED_SCHOOLS.map(school => (
                                <div key={school.id} className="bg-white p-5 rounded-3xl border shadow-sm hover:shadow-md transition-shadow group">
                                    <div className="flex justify-between items-start mb-4">
                                        <div
                                            className="w-12 h-12 rounded-2xl flex items-center justify-center text-white"
                                            style={{ backgroundColor: school.color }}
                                        >
                                            <Building2 className="w-6 h-6" />
                                        </div>
                                        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button className="p-2 text-gray-400 hover:text-indigo-600 rounded-xl hover:bg-indigo-50 transition-colors">
                                                <Settings2 className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 text-gray-400 hover:text-red-500 rounded-xl hover:bg-red-50 transition-colors">
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>

                                    <h4 className="text-lg font-bold text-gray-900">{school.name}</h4>
                                    <p className="text-sm text-gray-500 mt-1">{school.atpt_code} · {school.sd_code}</p>

                                    <div className="mt-6 flex items-center justify-between">
                                        <div className="space-y-1">
                                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-tighter">마지막 동기화</p>
                                            <p className="text-xs font-semibold text-gray-700">12분 전</p>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <div className="w-10 h-6 bg-indigo-600 rounded-full relative cursor-pointer">
                                                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Sidebar Status Info */}
                <div className="space-y-6">
                    <div className="bg-white/40 backdrop-blur-sm p-6 rounded-3xl border border-gray-100 space-y-4 shadow-sm">
                        <h3 className="text-base font-bold text-gray-800">동기화 상태</h3>
                        <div className="space-y-3">
                            <div className="flex items-center gap-3 p-3 bg-white rounded-2xl border border-gray-100">
                                <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-bold">NEIS API 연결됨</p>
                                    <p className="text-[11px] text-gray-400">지연 시간: 45ms</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-3 p-3 bg-white rounded-2xl border border-gray-100">
                                <RefreshCw className="w-5 h-5 text-indigo-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-bold">자동 동기화 활성</p>
                                    <p className="text-[11px] text-gray-400">매 6시간마다 갱신</p>
                                </div>
                            </div>
                        </div>

                        <button className="w-full py-3 bg-white border-2 border-dashed border-gray-200 rounded-2xl text-sm font-bold text-gray-500 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50/50 transition-all flex items-center justify-center gap-2">
                            <RefreshCw className="w-4 h-4" />
                            전체 강제 동기화
                        </button>
                    </div>

                    <div className="bg-indigo-600 p-6 rounded-3xl text-white shadow-xl shadow-indigo-200 relative overflow-hidden group">
                        <div className="absolute -bottom-8 -right-8 opacity-10 group-hover:scale-110 transition-transform duration-700">
                            <Building2 className="w-32 h-32" />
                        </div>
                        <h3 className="text-lg font-bold mb-2 relative z-10">알려진 이슈</h3>
                        <p className="text-sm opacity-90 relative z-10">일부 특수/영재학교의 경우 학사일정 제공 범위가 다를 수 있습니다.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SchoolSchedulePage;
