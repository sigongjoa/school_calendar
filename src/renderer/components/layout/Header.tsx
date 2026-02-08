import { Calendar, Building2 } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import clsx from 'clsx';

export const Header = () => {
    return (
        <header className="h-14 bg-white border-b flex items-center px-4 justify-between select-none">
            <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-lg font-bold text-gray-800">학사일정 캘린더</h1>
            </div>

            <nav className="flex gap-1 bg-gray-100 p-1 rounded-lg">
                <NavLink
                    to="/"
                    className={({ isActive }) =>
                        clsx(
                            'px-4 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            isActive
                                ? 'bg-white text-indigo-700 shadow-sm'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200'
                        )
                    }
                >
                    <Calendar className="w-4 h-4" />
                    캘린더
                </NavLink>
                <NavLink
                    to="/schools"
                    className={({ isActive }) =>
                        clsx(
                            'px-4 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            isActive
                                ? 'bg-white text-indigo-700 shadow-sm'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200'
                        )
                    }
                >
                    <Building2 className="w-4 h-4" />
                    학교 관리
                </NavLink>
            </nav>
        </header>
    );
};
