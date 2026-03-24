import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Activity, LayoutList, PlusCircle, Settings, HelpCircle, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isActive = (path: string) =>
    location.pathname === path
      ? 'bg-red-50 text-red-600 border-r-4 border-red-600'
      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900';

  return (
    <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 flex flex-col z-50">
      <div className="flex items-center h-16 px-6 border-b border-gray-200">
        <Link to={isAuthenticated ? `/dashboard/${user?.role.toLowerCase()}` : '/'} className="flex items-center gap-3">
          <div className="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold">🔥</span>
          </div>
          <span className="font-bold text-xl text-gray-900">BurnCare AI</span>
        </Link>
      </div>

      {isAuthenticated && user && (
        <div className="px-6 py-4 border-b border-gray-200">
          <p className="text-sm font-medium text-gray-900">{user.name}</p>
          <p className="text-xs text-gray-500 mt-1">{user.role}</p>
          <p className="text-xs text-gray-500">{user.email}</p>
        </div>
      )}

      <div className="flex-1 flex flex-col py-6 overflow-y-auto">
        {isAuthenticated && (
          <nav className="space-y-1">
            <Link
              to="/patients"
              className={`flex items-center px-6 py-3 text-sm font-medium transition-colors ${isActive('/patients')}`}
            >
              <LayoutList className="w-5 h-5 mr-3" />
              Patient Registry
            </Link>
            <Link
              to="/triage"
              className={`flex items-center px-6 py-3 text-sm font-medium transition-colors ${isActive('/triage')}`}
            >
              <Activity className="w-5 h-5 mr-3" />
              Triage Dashboard
            </Link>
          </nav>
        )}
      </div>

      {isAuthenticated && (
        <div className="border-t border-gray-200 px-6 py-4">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>
      )}
    </aside>
  );
};