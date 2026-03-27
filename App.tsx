import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { PatientForm } from './components/PatientForm';
import { PatientList } from './components/PatientList';
import { PatientDetail } from './components/PatientDetail';
import { TriageDashboard } from './components/TriageDashboard';
import Landing from './components/Landing';
import Login from './components/Login';
import Signup from './components/Signup';
import ChangePassword from './components/ChangePassword';
import ProtectedRoute from './components/ProtectedRoute';
import AdminPanel from './components/AdminPanel';
import { AuthProvider } from './context/AuthContext';

const DoctorDashboard: React.FC = () => (
  <div className="flex min-h-screen bg-gray-50">
    <Navbar />
    <main className="flex-1 ml-64 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Doctor Dashboard</h1>
      <TriageDashboard />
    </main>
  </div>
);

const AdminDashboard: React.FC = () => (
  <div className="flex min-h-screen bg-gray-50">
    <Navbar />
    <main className="flex-1 ml-64 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Hospital Administration</h1>
      <AdminPanel />
    </main>
  </div>
);

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/change-password" element={<ChangePassword />} />

          {/* Protected Routes - Doctor Dashboard */}
          <Route
            path="/dashboard/doctor"
            element={
              <ProtectedRoute allowedRoles={['Doctor']}>
                <DoctorDashboard />
              </ProtectedRoute>
            }
          />

          {/* Protected Routes - Admin Dashboard */}
          <Route
            path="/dashboard/admin"
            element={
              <ProtectedRoute allowedRoles={['Admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          {/* Original Patient Routes (for testing) */}
          <Route
            path="/patients/new"
            element={
              <ProtectedRoute allowedRoles={['Doctor', 'Admin']}>
                <PatientForm />
              </ProtectedRoute>
            }
          />
          <Route path="/patients" element={<PatientList />} />
          <Route path="/patient/:id" element={<PatientDetail />} />
          <Route path="/triage" element={<TriageDashboard />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;